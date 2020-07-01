CREATE TABLE public.list
(
  id                      bigserial NOT NULL,
  title                   text      NOT NULL,
  page_url                text      NOT NULL,
  type                    text,
  image_url               text,
  wikipedias_by_languages jsonb DEFAULT '{}'::jsonb,
  titles_by_languages     jsonb DEFAULT '{}'::jsonb,
  parent_page_url         text,
  parent_id               bigint,
  CONSTRAINT pk_list PRIMARY KEY (id),
  CONSTRAINT uq_page_url UNIQUE (page_url),
  CONSTRAINT fk_list_parent_id FOREIGN KEY (parent_id) REFERENCES public.list (id)
);

CREATE INDEX ix_list
  ON public.list (parent_id, "type");