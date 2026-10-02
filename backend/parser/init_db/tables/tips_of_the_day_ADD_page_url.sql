DO $$
  BEGIN
    IF NOT EXISTS(
        SELECT 1
        FROM pg_class tbl
               INNER JOIN pg_attribute col ON col.attrelid = tbl.oid
        WHERE tbl.relname = 'tips_of_the_day'
          AND col.attname = 'page_id') THEN
      ALTER TABLE public.tips_of_the_day
        ADD COLUMN page_id text REFERENCES public.list (page_id);
    END IF;
  END
$$
LANGUAGE plpgsql;