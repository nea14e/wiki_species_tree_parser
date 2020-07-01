CREATE TABLE public.ranks
(
       type    text NOT NULL
              CONSTRAINT ranks_pk PRIMARY KEY,
       "order" int  NOT NULL,
       titles_by_languages jsonb DEFAULT '{}'::jsonb
);

CREATE UNIQUE INDEX ix_unique_ranks
       ON public.ranks ("order");
