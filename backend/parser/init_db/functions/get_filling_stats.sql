CREATE OR REPLACE FUNCTION public.get_filling_stats(_groups_count int, _nested_level int, _outer_group_number int, _is_test_data boolean = FALSE)
  RETURNS json
  STABLE
AS
$$
  /*
         Хранимка по выдаче статистики заполнения таблицы животных парсером

         _groups_count - количество групп на каждом уровне
         _nested_level - уровень вложенности (начиная с 0, не включая сам открываемый уровень)
         _outer_group_number - номер группы, внутренности которой хотим открыть (сквозная нумерация с 1 на уровне, предыдущем открываемому), или NULL для корня
         _is_test_data - использовать ли генерацию тестовых данных или же таблицу с животными из БД

         Например, если иерархия групп такая:
         ---
           --
           --
           --
         ---   - если мы раскрываем эту группу, то _groups_count = 3, _nested_level = 1, _outer_group_number = 2
           --  - если мы раскрываем эту группу, то _groups_count = 3, _nested_level = 2, _outer_group_number = 4
           --
           --
         ---
           --
           --
           --
   */
SELECT json_agg(t_result ORDER BY group_number)
FROM (
       SELECT group_number,
              title_from,
              title_to,
              total,
              stage_2,
              public.percent_of(stage_2, total) AS stage_2_percent,
              public.percent_of_to_color(stage_2, total) AS stage_2_color,
              stage_3,
              public.percent_of(stage_3, total) AS stage_3_percent,
              public.percent_of_to_color(stage_3, total) AS stage_3_color,
              stage_4,
              public.percent_of(stage_4, total) AS stage_4_percent,
              public.percent_of_to_color(stage_4, total) AS stage_4_color
       FROM (
              SELECT group_number,
                     min(title)                                        AS title_from,
                     max(title)                                        AS title_to,
                     count(1)                                          AS total,
                     count(1) FILTER ( WHERE "type" IS NOT NULL)       AS stage_2,
                     count(1) FILTER ( WHERE parent_id IS NOT NULL)    AS stage_3,
                     count(1) FILTER ( WHERE leaves_count IS NOT NULL) AS stage_4
              FROM (
                     SELECT title,
                            "type",
                            parent_id,
                            leaves_count,
                            ntile(_groups_count) OVER () +
                            coalesce(_outer_group_number - 1, 0) * _groups_count AS group_number -- сквозная нумерация групп на текущем уровне
                     FROM (
                            /*
                                   Тестовые данные:
                                   названия 0 - 9999,
                                   до 2000 все заполнены,
                                   от 2000 до 2100 плавно уменьшаются проценты заполнения всех этапов,
                                   так, что каждый последующий этап заполнен меньше, чем предыдущий,
                                   к 2100 и позже уже совсем ничего не заполнено.
                             */
                            SELECT 'test_' || lpad(ser.i::text, 4, '0') AS title,
                                   CASE WHEN ser.i % 10 < 10 - (ser.i - 2000) / 10 THEN 'type123' END        AS "type",
                                   CASE WHEN ser.i % 10 < 10 - 2 * (ser.i - 2000) / 10 THEN 123::bigint END  AS parent_id,
                                   CASE WHEN ser.i % 10 < 10 - 3 * (ser.i - 2000) / 10 THEN 123::bigint END  AS leaves_count,
                                   ntile(power(_groups_count, _nested_level)::int) OVER (ORDER BY ser.i)     AS outer_group_number
                            FROM generate_series(0, 9999) ser(i)
                            WHERE _is_test_data = TRUE
                            UNION ALL
                            -- Реальная таблица из БД:
                            SELECT title,
                                   "type",
                                   parent_id,
                                   leaves_count,
                                   ntile(power(_groups_count, _nested_level)::int) OVER (ORDER BY title)    AS outer_group_number
                            FROM public.list
                            WHERE _is_test_data = FALSE
                          ) t_source
                     WHERE (outer_group_number = _outer_group_number OR _outer_group_number IS NULL)
                   ) t_filtered
              GROUP BY group_number
            ) t_counts
     ) t_result;
$$ LANGUAGE SQL;

/*
 -- Тесты хранимки:

 -- Корневая страница, 10 групп, таблица в БД
 SELECT public.get_filling_stats(
       _groups_count := 10,
       _nested_level := 0,
       _outer_group_number := NULL,
       _is_test_data := FALSE
 );

 -- Корневая страница, 10 групп, сгенерированные данные
 SELECT public.get_filling_stats(
       _groups_count := 10,
       _nested_level := 0,
       _outer_group_number := NULL,
       _is_test_data := TRUE
 );

 -- Корневая страница, 20 групп (группа меньше - процент заполнения больше при том же количестве)
 SELECT public.get_filling_stats(
       _groups_count := 20,
       _nested_level := 0,
       _outer_group_number := NULL,
       _is_test_data := TRUE
 );

 -- Вложенная страница, 2000 - 3000 (разбили на 10 групп по 1000 - это 1-ый уровень; взяли в нём 3-ю группу и разбили её на 10 групп по 100 - получили текущий уровень; всего на нём 10*10 групп, поэтому номера двузначные)
 SELECT public.get_filling_stats(
       _groups_count := 10,
       _nested_level := 1,
       _outer_group_number := 3,
       _is_test_data := TRUE
 );

 -- Вложенная-вложенная страница, 2000 - 2100 (с предыдущей страницы взяли 21-ую группу и разбили её ещё на 10 групп по 10)
 SELECT public.get_filling_stats(
       _groups_count := 10,
       _nested_level := 2,
       _outer_group_number := 21,
       _is_test_data := TRUE
 );

 -- Пустая вложенная-вложенная страница, 2300 - 2400 (оттуда же 25-ая группа)
 SELECT public.get_filling_stats(
       _groups_count := 10,
       _nested_level := 2,
       _outer_group_number := 25,
       _is_test_data := TRUE
 );

  */