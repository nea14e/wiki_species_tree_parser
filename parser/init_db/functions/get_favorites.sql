CREATE OR REPLACE FUNCTION public.get_favorites(_ids bigint[], _language_key text DEFAULT NULL::text)
  RETURNS json
  STABLE
  LANGUAGE SQL
AS
$$
SELECT json_agg(t ORDER BY title_for_language)
FROM (
       SELECT list.id,
              COALESCE(ranks.titles_by_languages ->> _language_key, ranks."type") AS rank_for_language,  -- Latin name if not present
              COALESCE(list.titles_by_languages ->> _language_key, list.title)    AS title_for_language, -- Latin name if not present
              list.image_url,
              list.leaves_count
       FROM public.list
              LEFT JOIN public.ranks ON list."type" = ranks."type"
       WHERE list.id = ANY (_ids)
     ) t;
$$;