CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS public.synonyms
(
  id                uuid PRIMARY KEY DEFAULT (uuid_generate_v4()),
  title             text   NOT NULL,
  type              text,
  parent_page_url   text,
  page_url_synonyms text[] NOT NULL,
  result_page_url   text
);


CREATE OR REPLACE FUNCTION public.find_synonyms()
  RETURNS void
  VOLATILE
AS
$$
DECLARE
BEGIN
  INSERT INTO public.synonyms(id, title, type, parent_page_url, page_url_synonyms)
  SELECT uuid_generate_v4(), title, type, parent_page_url, array_agg(page_url)
  FROM public.list
  WHERE title >= 'A'  -- exclude '-' titles and etc.
  GROUP BY title, type, parent_page_url
  HAVING count(1) >= 2;
END;
$$
  LANGUAGE plpgsql;


TRUNCATE public.synonyms;

SELECT public.find_synonyms();

DROP FUNCTION IF EXISTS public.find_synonyms();

/*
SELECT *
FROM public.synonyms
ORDER BY synonyms.title;
*/