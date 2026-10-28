ALTER TABLE public.list
    ADD COLUMN IF NOT EXISTS latin text;

-- Индекс ix_list_for_latin_search использует title,
-- где теперь хранится название на главном языке парсинга,
-- поэтому оставляем его.
ALTER INDEX IF EXISTS ix_list_for_latin_search
    RENAME TO ix_list_for_title_search;

CREATE INDEX IF NOT EXISTS ix_list_for_latin_search_2
    ON public.list(upper(latin));