-- noinspection SqlWithoutWhere
DELETE FROM public.ranks;

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('1st', -10, '{"en": "First level", "ru": "Первый уровень"}', true);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('2nd', -20, '{"en": "Second level (irregular)", "ru": "Второй уровень (нерегулярный)"}', false);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('3rd', -30, '{"en": "Third level", "ru": "Третий уровень"}', true);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('4th', -40, '{"en": "Forth level", "ru": "Четвёртый уровень"}', true);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('5th', -50, '{"en": "Fifth level", "ru": "Пятый уровень"}', true);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('6th', -60, '{"en": "Sixth level", "ru": "Шестой уровень"}', true);
