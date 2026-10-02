-- Add column is_deleted boolean NOT NULL DEFAULT (FALSE):
DO $$
  BEGIN
    IF NOT EXISTS(
        SELECT 1
        FROM pg_class tbl
               INNER JOIN pg_attribute col ON col.attrelid = tbl.oid
        WHERE tbl.relname = 'list'
          AND col.attname = 'synonyms') THEN

        ALTER TABLE public.list
            ADD COLUMN synonyms text[];
        
        ALTER TABLE public.list
            ADD CONSTRAINT uq_list_page_id UNIQUE (page_id);

    END IF;
  END
$$
LANGUAGE plpgsql;

SELECT ARRAY ['title', 'synonyms']::text[]