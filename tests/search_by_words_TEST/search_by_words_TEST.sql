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
       SELECT ser.i                        AS id,
              public.random_text_simple(8) AS title,
              (random() < 0.5)::boolean    AS has_en,
              (random() < 0.5)::boolean    AS has_ru
       FROM generate_series(10000000, 10400000) ser("i") -- делаем 400 000 записей начиная с id = 10 000 000, чтоб с боевыми не путались.
     ) t
ON CONFLICT DO NOTHING;

-- Проверка вхождений какого-нибудь слова, на котором собираемся тестировать
SELECT DISTINCT list_item_id
FROM public.titles_by_languages_by_words
WHERE language_key = 'en'
  AND word ILIKE 'asd%' -- тут регистронезависимо
UNION
DISTINCT
SELECT DISTINCT id
FROM public.list
WHERE title ILIKE 'asd%' -- Латинские названия search_by_words() ищет по list.title
;

-- Проверка любого id
SELECT *
FROM public.list
WHERE id = 1350207;

-- Проверка нашей функции
SELECT jsonb_array_length(public.search_by_words('asd', 'en')::jsonb);
SELECT public.search_by_words('asd', 'en');

-- Удалить все накатанные в этом примере
DELETE
FROM public.list
WHERE id >= 1000;