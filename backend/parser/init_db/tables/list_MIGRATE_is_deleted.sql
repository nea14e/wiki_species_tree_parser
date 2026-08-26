-- Add column is_deleted boolean NOT NULL DEFAULT (FALSE):
DO $$
  BEGIN
    IF NOT EXISTS(
        SELECT 1
        FROM pg_class tbl
               INNER JOIN pg_attribute col ON col.attrelid = tbl.oid
        WHERE tbl.relname = 'list'
          AND col.attname = 'is_deleted') THEN

        ALTER TABLE public.list ADD COLUMN is_deleted boolean NOT NULL DEFAULT (FALSE);

    END IF;
  END
$$
LANGUAGE plpgsql;