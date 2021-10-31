DO $$
BEGIN
  IF NOT EXISTS(
      SELECT 1
      FROM public.known_languages
      WHERE is_main_for_admins = TRUE
    ) THEN

    UPDATE public.known_languages
    SET is_main_for_admins = TRUE
    WHERE lang_key = 'ru';

  END IF;
END;
$$ LANGUAGE plpgsql;
