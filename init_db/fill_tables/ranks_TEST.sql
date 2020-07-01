-- noinspection SqlWithoutWhere
DELETE FROM public.ranks;

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('1st', -10, '{"en": "First level", "ru": "Первый уровень"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('4th', -40, '{"en": "Forth level", "ru": "Четвёртый уровень"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('6th', -60, '{"en": "Sixth level", "ru": "Шестой уровень"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('3rd', -30, '{"en": "Third level", "ru": "Третий уровень"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('2nd', -20, '{"en": "Second level", "ru": "Второй уровень"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('5th', -50, '{"en": "Fifth level", "ru": "Пятый уровень"}');
