CREATE TABLE public.get_tree_cache
(
  id                  bigint PRIMARY KEY
    REFERENCES public.list(id),
  result_on_languages    jsonb NOT NULL
);