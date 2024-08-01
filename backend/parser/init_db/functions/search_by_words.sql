DROP FUNCTION IF EXISTS public.search_by_words(text, int, text);

CREATE OR REPLACE FUNCTION public.search_by_words(_query text, _limit int, _offset int, _language_key text DEFAULT NULL::text) RETURNS json
  STABLE
  LANGUAGE SQL
AS
$$
SELECT coalesce(json_agg(t ORDER BY rank_order DESC, title_for_language), '[]'::json)
FROM (
       SELECT max(list.id)            AS id,
              max(list.page_url)      AS page_url,
              COALESCE(ranks.titles_by_languages ->> _language_key, ranks."type") AS rank_for_language,  -- Latin name if not present
              COALESCE(list.titles_by_languages ->> _language_key, list.title)    AS title_for_language, -- Latin name if not present
              max(list.image_url)     AS image_url,
              max(ranks."order")      AS rank_order,
              max(list.leaves_count)  AS leaves_count
       FROM public.list
              LEFT JOIN public.ranks ON list."type" = ranks."type"
       WHERE (
             upper(list.titles_by_languages ->> _language_key) LIKE (upper(_query) || '%')
           AND _language_key IS NOT NULL
         )
          OR (
         upper(list.title) LIKE (upper(_query) || '%') -- support Latin for any _language_key (Note: here can be used "ix_list_for_latin_search" functional index)
         )
       GROUP BY rank_for_language, title_for_language  -- удаление дубликатов (синонимов). Синонимы невозможно отсечь через is_deleted, т.к. пользователь может искать именно синоним.
       ORDER BY rank_order DESC, title_for_language
       LIMIT _limit + 1 OFFSET _offset
     ) t;
$$;