CREATE TABLE public.known_languages
(
  lang_key            text
    CONSTRAINT pk_known_languages
      PRIMARY KEY,
  "comment"           text NOT NULL DEFAULT '',
  site_title          text NOT NULL DEFAULT '',
  site_description    text NOT NULL DEFAULT '',
  parent_word         text NOT NULL DEFAULT '',
  rank_word           text NOT NULL DEFAULT '',
  search_word         text NOT NULL DEFAULT '',
  tip_of_the_day_word text NOT NULL DEFAULT '',
  authors_word        text NOT NULL DEFAULT '',
  authors_content     text NOT NULL DEFAULT ''
);

-- ==============================================================================================================
-- ==============================================================================================================

CREATE OR REPLACE FUNCTION public.tg_update_language_index()
  RETURNS trigger AS
$$
DECLARE
  _sql text;
BEGIN
  IF tg_op = 'INSERT' THEN
    -- Create index for new language
    _sql = 'CREATE INDEX IF NOT EXISTS ix_list_titles_by_languages_' || NEW.lang_key ||
           ' ON public.list ((upper(titles_by_languages->>''' || NEW.lang_key || ''')));';
    EXECUTE (_sql);
    RETURN NEW;
  ELSEIF
    tg_op = 'UPDATE' THEN
    IF NEW.lang_key != OLD.lang_key THEN
      -- Remove index for deleted language
      _sql = 'DROP INDEX IF EXISTS ix_list_titles_by_languages_' || OLD.lang_key || ';';
      EXECUTE (_sql);
      -- Create index for new language
      _sql = 'CREATE INDEX IF NOT EXISTS ix_list_titles_by_languages_' || NEW.lang_key ||
             ' ON public.list ((upper(titles_by_languages->>''' || NEW.lang_key || ''')));';
      EXECUTE (_sql);
    END IF;
    RETURN NEW;
  ELSE -- DELETE/TRUNCATE
  -- Remove index for deleted language
    _sql = 'DROP INDEX IF EXISTS ix_list_titles_by_languages_' || OLD.lang_key || ';';
    EXECUTE (_sql);
    RETURN NULL;
  END IF;
END;
$$ LANGUAGE 'plpgsql';

-- ==============================================================================================================
-- ==============================================================================================================

CREATE TRIGGER trig_update_language_index
  AFTER INSERT OR UPDATE OR DELETE
  ON public.known_languages
  FOR EACH ROW
EXECUTE PROCEDURE public.tg_update_language_index();
