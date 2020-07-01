CREATE FUNCTION search_by_words(_query text, _language_key text DEFAULT NULL::text) RETURNS json
  LANGUAGE SQL
AS
$$
SELECT json_agg(t ORDER BY rank_order DESC, title_for_language ASC)
FROM (
       SELECT list.id,
              COALESCE(ranks.titles_by_languages ->> _language_key, ranks."type") AS rank_for_language,  -- Latin name if not present
              COALESCE(list.titles_by_languages ->> _language_key, list.title)    AS title_for_language, -- Latin name if not present
              list.image_url,
              ranks."order"                                                       AS rank_order
       FROM public.list
              LEFT JOIN public.ranks ON list."type" = ranks."type"
       WHERE list.id IN (
         SELECT w.list_item_id
         FROM public.titles_by_languages_by_words w
         WHERE (w.language_key = _language_key OR _language_key IS NULL) -- use chosen or any language
           AND w.word LIKE (upper(_query) || '%')
       )
          OR upper(list.title) LIKE (upper(_query) || '%') -- support Latin for any _language_key (Note: here can be used "ix_list_for_latin_search" functional index)
     ) t;
$$;

ALTER FUNCTION search_by_words(text, text) OWNER TO postgres;

