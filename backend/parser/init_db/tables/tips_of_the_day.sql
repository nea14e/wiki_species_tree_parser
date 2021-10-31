CREATE TABLE public.tips_of_the_day
(
  id                  serial PRIMARY KEY,
  tip_on_languages    jsonb NOT NULL
);