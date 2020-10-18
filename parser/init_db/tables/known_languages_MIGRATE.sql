DO $$
  BEGIN
    IF EXISTS(
        SELECT 1
        FROM pg_class tbl
               INNER JOIN pg_attribute col ON col.attrelid = tbl.oid
        WHERE tbl.relname = 'known_languages'
          AND col.attname = 'site_title') THEN

      ALTER TABLE public.known_languages DROP COLUMN site_title;
      ALTER TABLE public.known_languages DROP COLUMN site_description;
      ALTER TABLE public.known_languages DROP COLUMN parent_word;
      ALTER TABLE public.known_languages DROP COLUMN rank_word;
      ALTER TABLE public.known_languages DROP COLUMN search_word;
      ALTER TABLE public.known_languages DROP COLUMN tip_of_the_day_word;
      ALTER TABLE public.known_languages DROP COLUMN authors_word;
      ALTER TABLE public.known_languages DROP COLUMN authors_content;

      ALTER TABLE public.known_languages ADD COLUMN translations jsonb DEFAULT '{}'::jsonb;

    END IF;
  END
$$
LANGUAGE plpgsql;