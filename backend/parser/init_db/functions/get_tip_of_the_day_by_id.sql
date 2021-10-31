CREATE OR REPLACE FUNCTION public.get_tip_of_the_day_by_id(_language_key text, _id integer)
  RETURNS json
  STABLE
  LANGUAGE SQL
AS
$$
  SELECT json_agg(t)->0
  FROM (
    SELECT
      t.id,
      COALESCE(
          t.tip_on_languages ->> _language_key,
          t.tip_on_languages ->> 'en'
        ) AS tip_text,
      list.id AS species_id,
      list.image_url
    FROM public.tips_of_the_day t
      LEFT JOIN public.list list ON t.page_url = list.page_url
    WHERE t.id = _id
    LIMIT 1
  ) t;
$$;