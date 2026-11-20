DO $$
  BEGIN
    IF NOT EXISTS(
        SELECT 1
        FROM pg_class tbl
               INNER JOIN pg_attribute col ON col.attrelid = tbl.oid
        WHERE tbl.relname = 'tips_of_the_day'
          AND col.attname = 'list_id') THEN
                            
      ALTER TABLE public.tips_of_the_day
        ADD COLUMN IF NOT EXISTS list_id bigint;
        
      ALTER TABLE public.tips_of_the_day
        ADD CONSTRAINT fk_tips_of_the_day_list_id FOREIGN KEY (list_id) REFERENCES public.list(id);
        
    END IF;
  END
$$
LANGUAGE plpgsql;