-- Add column last_error_message text:
DO $$
  BEGIN
    IF NOT EXISTS(
        SELECT 1
        FROM pg_class tbl
               INNER JOIN pg_attribute col ON col.attrelid = tbl.oid
        WHERE tbl.relname = 'list'
          AND col.attname = 'last_error_message') THEN

        ALTER TABLE public.list ADD COLUMN last_error_message text;

    END IF;
  END
$$
LANGUAGE plpgsql;