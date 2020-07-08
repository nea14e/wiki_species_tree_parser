-- Штампуем записи
INSERT INTO public.list(id, title, page_url, titles_by_languages)
SELECT t.id,
       t.title,
       t.title || '_url' AS page_url,
       CASE
         WHEN t.has_en AND t.has_ru THEN
           jsonb_build_object(
               'en', public.random_text('en', 8) || ' ' || public.random_text('en', 8),
               'ru', public.random_text('ru', 8) || ' ' || public.random_text('ru', 8)
             )
         WHEN t.has_en AND NOT t.has_ru THEN
           jsonb_build_object(
               'en', public.random_text('en', 8) || ' ' || public.random_text('en', 8)
             )
         WHEN NOT t.has_en AND t.has_ru THEN
           jsonb_build_object(
               'ru', public.random_text('ru', 8) || ' ' || public.random_text('ru', 8)
             )
         ELSE
           '{}'::jsonb
         END             AS titles_by_languages
FROM (
       SELECT ser.i                       AS id,
              public.random_text('en', 8) AS title,
              (random() < 0.5)::boolean   AS has_en,
              (random() < 0.5)::boolean   AS has_ru
       FROM generate_series(10000000, 10400000) ser("i") -- делаем 400 000 записей начиная с id = 10 000 000, чтоб с боевыми не путались.
     ) t
ON CONFLICT DO NOTHING;

-- Проверка количества после штамповки
SELECT count(1)
FROM public.list;

-- Проверка вхождений какого-нибудь слова, на котором собираемся тестировать
SELECT DISTINCT id
FROM public.list
WHERE upper(titles_by_languages ->> 'ru') LIKE (upper('аб') || '%') -- тут регистронезависимо
  OR upper(title) LIKE (upper('аб') || '%'); -- Латинские названия search_by_words() ищет по list.title

-- Проверка любого id
SELECT *
FROM public.list
WHERE id = 10272057;

-- Проверка нашей функции
SELECT jsonb_array_length(public.search_by_words('аб', 'ru')::jsonb);
SELECT public.search_by_words('аб', 'ru');

-- Удалить все накатанные в этом примере
DELETE
FROM public.list
WHERE id >= 10000000;