create table public.known_languages
(
	lang_key text
		constraint pk_known_languages
			primary key,
	"comment" text
);