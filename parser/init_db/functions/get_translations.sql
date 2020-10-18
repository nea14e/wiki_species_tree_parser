CREATE OR REPLACE FUNCTION public.get_translations(_language_key text) RETURNS json
  STABLE
  LANGUAGE SQL
AS
$$
WITH translated_cte AS (
  SELECT t.lang_key,
         t.comment,
         t.translations
  FROM public.known_languages t
  WHERE t.lang_key = _language_key -- get translation if exists
  LIMIT 1
),
     english_cte AS (
       SELECT e.lang_key,
              e.comment,
              e.translations
       FROM public.known_languages e
       WHERE e.lang_key = 'en' -- get english
       LIMIT 1
     )
SELECT json_agg(t)->0
FROM (
       SELECT t.lang_key,
              t.comment,
              e.translations || t.translations as translations  -- get default values from English and override them by selected language
       FROM translated_cte t
          CROSS JOIN english_cte e
       UNION ALL
       SELECT e.lang_key,
              e.comment,
              e.translations AS translations
       FROM english_cte e
       WHERE NOT EXISTS(SELECT 1
                        FROM translated_cte)
     ) t;
$$;

ALTER FUNCTION get_tip_of_the_day(text) OWNER TO postgres;

