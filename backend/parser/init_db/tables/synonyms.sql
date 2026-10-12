ALTER TABLE public.list
    DROP COLUMN IF EXISTS synonyms;

-- Таблица с названиями на разных языках
-- Один и тот же вид может иметь несколько названий на одном языке
CREATE TABLE public.synonyms
(
    lang_key text NOT NULL
        CONSTRAINT fk_synonyms_lang_key REFERENCES public.known_languages(lang_key),
    list_id bigint NOT NULL
        CONSTRAINT fk_synonyms_list_id REFERENCES public.list(id),
    title text NOT NULL,
    -- PRIMARY KEY, он же индекс для поиска по id
    CONSTRAINT pk_synonyms PRIMARY KEY (lang_key, list_id, title)
);

-- Индекс для поиска по title
CREATE INDEX ix_synonyms_by_title ON public.synonyms(lang_key, title, list_id);

