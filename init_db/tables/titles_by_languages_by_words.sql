CREATE TABLE public.titles_by_languages_by_words
(
  list_item_id bigint NOT NULL
    REFERENCES public.list (id) ON DELETE CASCADE,
  language_key text   NOT NULL,
  word         text   NOT NULL,
  CONSTRAINT pk_titles_by_languages_by_words
    PRIMARY KEY (list_item_id, language_key, word)
);

CREATE INDEX ix_titles_by_words
  ON public.titles_by_languages_by_words (word, list_item_id);  -- include list_item_id to the index to speed up select

CREATE INDEX ix_titles_by_languages_by_words
  ON public.titles_by_languages_by_words (language_key, word, list_item_id);  -- include list_item_id to the index to speed up select



-- =============================================================================================================================================
-- =============================================================================================================================================
-- =============================================================================================================================================



CREATE FUNCTION tg_titles_by_languages_by_words() RETURNS trigger
  LANGUAGE plpgsql
AS
$$
BEGIN
  IF tg_op = 'INSERT' THEN
    INSERT INTO public.titles_by_languages_by_words(list_item_id, language_key, word)
    SELECT NEW.id,
           language_key,
           unnest(string_to_array(upper(langs.title), ' ')) AS word -- split each language to separate words (then convert array -> table with "unnest()")
    FROM jsonb_each_text(NEW.titles_by_languages) langs(language_key, title); -- split to languages

    RETURN NEW;
  ELSE
    IF tg_op = 'UPDATE' THEN

      IF NEW.titles_by_languages IS NOT DISTINCT FROM OLD.titles_by_languages THEN
        RETURN NEW;
      END IF;

      DELETE
      FROM public.titles_by_languages_by_words
      WHERE list_item_id = OLD.id;

      INSERT INTO public.titles_by_languages_by_words(list_item_id, language_key, word)
      SELECT NEW.id,
             language_key,
             unnest(string_to_array(upper(langs.title), ' ')) AS word -- split each language to separate words (then convert array -> table with "unnest()")
      FROM jsonb_each_text(NEW.titles_by_languages) langs(language_key, title); -- split to separate languages

      RETURN NEW;
    ELSE -- for DELETE/TRUNCATE
      DELETE
      FROM public.titles_by_languages_by_words
      WHERE list_item_id = OLD.id;

      RETURN NULL;
    END IF;
  END IF;
END;
$$;

ALTER FUNCTION tg_titles_by_languages_by_words() OWNER TO postgres;



-- =============================================================================================================================================
-- =============================================================================================================================================
-- =============================================================================================================================================



CREATE TRIGGER trig_titles_by_languages_by_words
  AFTER INSERT OR UPDATE OR DELETE -- after insertion! Otherwise will be foreign key error in public.titles_by_languages_by_words!
  ON public.list
  FOR EACH ROW
EXECUTE PROCEDURE public.tg_titles_by_languages_by_words();