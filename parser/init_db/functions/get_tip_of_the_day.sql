CREATE OR REPLACE FUNCTION public.get_tip_of_the_day(_language_key text)
  RETURNS json
  STABLE
  LANGUAGE SQL
AS
$$
  SELECT json_agg(t)
  FROM (
    SELECT
           id,
           tip_on_languages ->> _language_key AS tip_text
    FROM public.tips_of_the_day
    WHERE (  -- get translated tips only or any tips (when translated tips are not present for chosen language at all)
        tip_on_languages ? _language_key
        OR NOT EXISTS(SELECT 1
                      FROM public.tips_of_the_day
                      WHERE tip_on_languages ? _language_key)
      )
    ORDER BY random()
    LIMIT 1
  ) t;
$$;