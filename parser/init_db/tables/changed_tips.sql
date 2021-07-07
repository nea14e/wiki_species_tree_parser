CREATE TABLE public.changed_tips (
  tip_id int NOT NULL
    REFERENCES public.tips_of_the_day(id),
  lang_key text  -- NULL for general tip edit
    REFERENCES public.known_languages(lang_key),
  admin_user_id int  -- NULL for super-admin
    REFERENCES public.admin_users(id),
  read_by_user_ids jsonb DEFAULT '[]'::jsonb
);

CREATE UNIQUE INDEX IF NOT EXISTS uq_changed_tips_with_lang
  ON public.changed_tips (tip_id, lang_key)
  WHERE lang_key IS NOT NULL;

CREATE UNIQUE INDEX IF NOT EXISTS uq_changed_tips_without_lang
  ON public.changed_tips (tip_id)
  WHERE lang_key IS NULL;