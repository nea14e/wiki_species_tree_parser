CREATE OR REPLACE FUNCTION public.get_filling_stats(_page_url_from text, _page_url_to text, _groups_count int, _is_test_data boolean = FALSE)
  RETURNS json
  STABLE
AS
$$
  /*
         Хранимка по выдаче статистики заполнения таблицы животных парсером
   */
SELECT coalesce(json_agg(t_result ORDER BY group_number), '[]'::json)
FROM (
       SELECT group_number,
              page_url_from,
              page_url_to,
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
                     min(page_url)                                     AS page_url_from,
                     max(page_url)                                     AS page_url_to,
                     count(1)                                          AS total,
                     count(1) FILTER ( WHERE "type" IS NOT NULL)       AS stage_2,
                     count(1) FILTER ( WHERE parent_id IS NOT NULL)    AS stage_3,
                     count(1) FILTER ( WHERE leaves_count IS NOT NULL) AS stage_4
              FROM (
                     SELECT page_url,
                            "type",
                            parent_id,
                            leaves_count,
                            ntile(_groups_count) OVER (ORDER BY page_url) AS group_number -- сквозная нумерация групп на текущем уровне
                     FROM (
                            /*
                                   Тестовые данные:
                                   названия 0 - 9999,
                                   до 2000 все заполнены,
                                   от 2000 до 2100 плавно уменьшаются проценты заполнения всех этапов,
                                   так, что каждый последующий этап заполнен меньше, чем предыдущий,
                                   к 2100 и позже уже совсем ничего не заполнено.
                             */
                            SELECT 'test_' || lpad(ser.i::text, 4, '0') AS page_url,
                                   CASE WHEN ser.i % 10 < 10 - (ser.i - 2000) / 10 THEN 'type123' END        AS "type",
                                   CASE WHEN ser.i % 10 < 10 - 2 * (ser.i - 2000) / 10 THEN 123::bigint END  AS parent_id,
                                   CASE WHEN ser.i % 10 < 10 - 3 * (ser.i - 2000) / 10 THEN 123::bigint END  AS leaves_count
                            FROM generate_series(0, 9999) ser(i)
                            WHERE _is_test_data = TRUE
                            UNION ALL
                            -- Реальная таблица из БД:
                            SELECT page_url,
                                   "type",
                                   parent_id,
                                   leaves_count
                            FROM public.list
                            WHERE _is_test_data = FALSE
                          ) t_source
                     WHERE (page_url >= _page_url_from OR _page_url_from IS NULL)
                       AND (page_url <= _page_url_to OR _page_url_to IS NULL)
                   ) t_filtered
              GROUP BY group_number
            ) t_counts
     ) t_result;
$$ LANGUAGE SQL;

/*
 -- Тесты хранимки:

 -- Корневая страница, 10 групп, таблица в БД
 SELECT public.get_filling_stats(
       _page_url_from := null,
       _page_url_to := null,
       _groups_count := 10,
       _is_test_data := FALSE
 );

 -- Корневая страница, 10 групп, сгенерированные данные
 SELECT public.get_filling_stats(
       _page_url_from := null,
       _page_url_to := null,
       _groups_count := 10,
       _is_test_data := TRUE
 );

 -- Корневая страница, 20 групп
 SELECT public.get_filling_stats(
       _page_url_from := null,
       _page_url_to := null,
       _groups_count := 20,
       _is_test_data := TRUE
 );

 -- Вложенная страница, 2000 - 3000
 SELECT public.get_filling_stats(
       _page_url_from := 'test_2000',
       _page_url_to := 'test_3000',
       _groups_count := 10,
       _is_test_data := TRUE
 );

 -- Вложенная-вложенная страница, 2000 - 2100
 SELECT public.get_filling_stats(
       _page_url_from := 'test_2000',
       _page_url_to := 'test_2100',
       _groups_count := 10,
       _is_test_data := TRUE
 );

 -- Пустая вложенная-вложенная страница
 SELECT public.get_filling_stats(
       _page_url_from := 'test_2300',
       _page_url_to := 'test_2400',
       _groups_count := 10,
       _is_test_data := TRUE
 );

 -- Вложенная-вложенная страница, 2000 - 2100
 SELECT public.get_filling_stats(
       _page_url_from := 'test_2000',
       _page_url_to := 'test_2007',
       _groups_count := 10,
       _is_test_data := TRUE
 );

  */