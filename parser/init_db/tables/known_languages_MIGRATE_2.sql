DO $do$
  BEGIN
    IF NOT EXISTS(
        SELECT 1
        FROM pg_class tbl
               INNER JOIN pg_attribute col ON col.attrelid = tbl.oid
        WHERE tbl.relname = 'known_languages'
          AND col.attname = 'is_main_for_admins') THEN

      ALTER TABLE public.known_languages
        ADD COLUMN IF NOT EXISTS is_main_for_admins boolean NOT NULL DEFAULT FALSE;

      EXECUTE $sql$
          CREATE OR REPLACE FUNCTION public.tg__known_languages__is_main_for_admins()
            RETURNS trigger AS
          $f$
          BEGIN
            IF new.is_main_for_admins = TRUE THEN
              UPDATE public.known_languages
              SET is_main_for_admins = FALSE
              WHERE (lang_key != new.lang_key OR new.lang_key IS NULL);
            END IF;
            RETURN NEW;
          END;
          $f$ LANGUAGE 'plpgsql';
        $sql$;

      CREATE TRIGGER trig__is_main_for_admins
        BEFORE INSERT OR UPDATE
        ON public.known_languages
        FOR EACH ROW
      EXECUTE PROCEDURE public.tg__known_languages__is_main_for_admins();

    END IF;
  END
$do$
LANGUAGE plpgsql;