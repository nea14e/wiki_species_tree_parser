DROP FUNCTION IF EXISTS public.search_by_words(text, int, text);

DROP FUNCTION IF EXISTS public.search_by_words(_query text, _limit int, _offset int, _language_key text);

CREATE OR REPLACE FUNCTION public.search_by_words(_query text, _limit int, _offset int, _language_key1 text, _language_key2 text DEFAULT NULL::text)
    RETURNS json
  STABLE
  LANGUAGE SQL
AS
$$
SELECT coalesce(json_agg(t ORDER BY rank_order DESC, title_for_language1), '[]'::json)
FROM (
       SELECT list.id            AS id,
              list.page_id      AS page_id,
              ranks.titles_by_languages ->> _language_key1 AS rank_for_language1,
              ranks."type" AS rank_latin,
              CASE
                  WHEN _language_key1 != 'latin' THEN list.titles_by_languages ->> _language_key1
                  ELSE list.latin
              END AS title_for_language1,
              CASE
                  WHEN _language_key2 = 'latin' THEN list.latin
                  WHEN _language_key2 IS NOT NULL THEN list.titles_by_languages ->> _language_key2
                  WHEN _language_key2 IS NULL THEN NULL
              END AS title_for_language2,
              list.latin AS title_latin,
              list.image_url     AS image_url,
              ranks."order"      AS rank_order,
              list.leaves_count  AS leaves_count
       FROM public.list
              LEFT JOIN public.ranks ON list."type" = ranks."type"
       WHERE (
           -- TODO ? использовать таблицу синонимов для поиска? Хотя индексы уже есть.
           _language_key1 != 'latin' AND
           upper(list.titles_by_languages ->> _language_key1) LIKE (upper(_query) || '%')
         )
          OR (
            _language_key2 IS NOT NULL AND _language_key2 != 'latin' AND
            upper(list.titles_by_languages ->> _language_key2) LIKE (upper(_query) || '%')
         )
          OR (
              upper(list.latin) LIKE (upper(_query) || '%')
           )
       ORDER BY rank_order DESC, title_for_language1
       LIMIT _limit + 1 OFFSET _offset
     ) t;
$$;