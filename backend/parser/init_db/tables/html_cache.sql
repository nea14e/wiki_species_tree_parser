CREATE TABLE public.html_cache
(
    id bigint
        CONSTRAINT pk_html_cache PRIMARY KEY 
        CONSTRAINT fk_html_cache_id REFERENCES public.list (id),
    infobox text NOT NULL
);

