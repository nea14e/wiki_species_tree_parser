CREATE OR REPLACE FUNCTION public.get_tip_of_the_day(_language_key text)
  RETURNS json
  STABLE
  LANGUAGE SQL
AS
$$
  WITH translated_cte AS (
    SELECT
      id,
      tip_on_languages ->> _language_key AS tip_text
    FROM public.tips_of_the_day
    WHERE tip_on_languages ? _language_key  -- get translated tips if exists
    ORDER BY random()
    LIMIT 1
  ),
  english_cte AS (
    SELECT
      t.id,
      t.tip_on_languages ->> 'en' AS tip_text
    FROM public.tips_of_the_day t
      LEFT JOIN translated_cte ON TRUE
    WHERE t.tip_on_languages ? 'en'
      AND translated_cte.id IS NULL  -- else get any tips on English
    ORDER BY random()
    LIMIT 1
  )
  SELECT json_agg(t)
  FROM (
    SELECT id, tip_text
    FROM translated_cte
    UNION ALL
    SELECT id, tip_text
    FROM english_cte
  ) t;
$$;