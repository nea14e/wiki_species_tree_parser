CREATE OR REPLACE FUNCTION public.get_all_tips_translations(_language_key text)
  RETURNS json
  STABLE
  LANGUAGE SQL
AS
$$
WITH admin_lang_cte AS (
  SELECT lang_key
  FROM public.known_languages
  WHERE is_main_for_admins = TRUE
  LIMIT 1
)
SELECT COALESCE(json_agg(t.* ORDER BY COALESCE(t.title_by_language, t.title_by_admin, t.title_by_latin), t.id), '[]')
FROM (
       SELECT ti.*,
              li.id                                              AS species_id,
              li.image_url,
              li.title                                           AS title_by_latin,
              li.titles_by_languages,
              li.wikipedias_by_languages,
              li.titles_by_languages ->> admin_lang_cte.lang_key AS title_by_admin,
              li.titles_by_languages ->> _language_key           AS title_by_language,
              r.titles_by_languages ->> admin_lang_cte.lang_key  AS rank_by_admin,
              r.titles_by_languages ->> _language_key            AS rank_by_language
       FROM public.tips_of_the_day ti
              LEFT JOIN PUBLIC.list li ON ti.page_url = li.page_url
              LEFT JOIN public.ranks r ON li.type = r.type
              LEFT JOIN admin_lang_cte ON TRUE
     ) t
$$;