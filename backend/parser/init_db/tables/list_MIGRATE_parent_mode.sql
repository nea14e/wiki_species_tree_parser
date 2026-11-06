-- ADD CONSTRAINT IF NOT EXISTS сделать нельзя, поэтому костыль:
DO $$
    BEGIN
        IF NOT EXISTS(
            SELECT 1
            FROM pg_class tbl
                     INNER JOIN pg_attribute col ON col.attrelid = tbl.oid
            WHERE tbl.relname = 'list'
              AND col.attname = 'named_ranks_only_parent_title') THEN
                  
            ALTER TABLE public.list
                ADD COLUMN named_ranks_only_parent_title text;
            ALTER TABLE public.list
                ADD COLUMN named_ranks_only_parent_type text;
            ALTER TABLE public.list
                ADD COLUMN named_ranks_only_parent_id bigint;
            ALTER TABLE public.list
                ADD CONSTRAINT fk_list_named_ranks_only_parent_id
                    FOREIGN KEY (named_ranks_only_parent_id) REFERENCES public.list(id);
            CREATE INDEX ix_list_named_ranks_only_parent_id 
                ON public.list (named_ranks_only_parent_id, named_ranks_only_parent_type);
            ALTER TABLE public.list
                ADD COLUMN named_ranks_only_leaves_count bigint;

            ALTER TABLE public.list
                ADD COLUMN regular_ranks_only_parent_title text;
            ALTER TABLE public.list
                ADD COLUMN regular_ranks_only_parent_type text;
            ALTER TABLE public.list
                ADD COLUMN regular_ranks_only_parent_id bigint;
            ALTER TABLE public.list
                ADD CONSTRAINT fk_list_regular_ranks_only_parent_id
                    FOREIGN KEY (regular_ranks_only_parent_id) REFERENCES public.list(id);
            CREATE INDEX ix_list_regular_ranks_only_parent_id
                ON public.list (regular_ranks_only_parent_id, regular_ranks_only_parent_type);
            ALTER TABLE public.list
                ADD COLUMN regular_ranks_only_leaves_count bigint;

        END IF;
    END
$$
LANGUAGE plpgsql;