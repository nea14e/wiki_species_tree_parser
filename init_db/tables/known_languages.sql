CREATE TABLE public.known_languages
(
  lang_key text
    CONSTRAINT pk_known_languages
      PRIMARY KEY,
  "comment" text NOT NULL DEFAULT ''
);