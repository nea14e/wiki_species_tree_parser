-- noinspection SqlWithoutWhere
DELETE FROM public.list;

INSERT INTO public.list (id, title, page_url, type, image_url, wikipedias_by_languages, titles_by_languages, parent_page_url, parent_id)
VALUES (2, 'B', 'B_url', '1st', null, '{"en": "B_en_url", "ru": "B_ru_url"}', '{"en": "B_en", "ru": "B_ru"}', null, null);

INSERT INTO public.list (id, title, page_url, type, image_url, wikipedias_by_languages, titles_by_languages, parent_page_url, parent_id)
VALUES (1, 'A', 'A_url', '1st', null, '{"en": "A_en_url", "ru": "A_ru_url"}', '{"en": "A_en", "ru": "A_ru"}', null, null);

INSERT INTO public.list (id, title, page_url, type, image_url, wikipedias_by_languages, titles_by_languages, parent_page_url, parent_id)
VALUES (12, 'Ab', 'Ab_url', '2nd', null, '{"en": "Ab_en_url", "ru": "Ab_ru_url"}', '{"en": "Ab_en", "ru": "Ab_ru"}', 'A_url', 1);

INSERT INTO public.list (id, title, page_url, type, image_url, wikipedias_by_languages, titles_by_languages, parent_page_url, parent_id)
VALUES (11, 'Aa', 'Aa_url', '2nd', null, '{"en": "Aa_en_url", "ru": "Aa_ru_url"}', '{"en": "Aa_en", "ru": "Aa_ru"}', 'A_url', 1);

INSERT INTO public.list (id, title, page_url, type, image_url, wikipedias_by_languages, titles_by_languages, parent_page_url, parent_id)
VALUES (22, 'Bb_without_languages', 'Bb_url', '2nd', null, '{}', '{}', 'B_url', 2);

INSERT INTO public.list (id, title, page_url, type, image_url, wikipedias_by_languages, titles_by_languages, parent_page_url, parent_id)
VALUES (21, 'Ba', 'Ba_url', '2nd', null, '{"en": "Ba_en_url", "ru": "Ba_ru_url"}', '{"en": "Ba_en", "ru": "Ba_ru"}', 'B_url', 2);

INSERT INTO public.list (id, title, page_url, type, image_url, wikipedias_by_languages, titles_by_languages, parent_page_url, parent_id)
VALUES (111, 'Aa1', 'Aa1_url', '3rd', null, '{"en": "Aa1_en_url", "ru": "Aa1_ru_url"}', '{"en": "Aa1_en", "ru": "Aa1_ru"}', 'Aa_url', 11);

INSERT INTO public.list (id, title, page_url, type, image_url, wikipedias_by_languages, titles_by_languages, parent_page_url, parent_id)
VALUES (112, 'Aa2', 'Aa2_url', '3rd', null, '{"en": "Aa2_en_url", "ru": "Aa2_ru_url"}', '{"en": "Aa2_en", "ru": "Aa2_ru"}', 'Aa_url', 11);

INSERT INTO public.list (id, title, page_url, type, image_url, wikipedias_by_languages, titles_by_languages, parent_page_url, parent_id)
VALUES (122, 'Ab2', 'Ab2_url', '3rd', null, '{"en": "Ab2_en_url", "ru": "Ab2_ru_url"}', '{"en": "Ab2_en", "ru": "Ab2_ru"}', 'Ab_url', 12);

INSERT INTO public.list (id, title, page_url, type, image_url, wikipedias_by_languages, titles_by_languages, parent_page_url, parent_id)
VALUES (121, 'Ab1', 'Ab1_url', '3rd', null, '{"en": "Ab1_en_url", "ru": "Ab1_ru_url"}', '{"en": "Ab1_en", "ru": "Ab1_ru"}', 'Ab_url', 12);

INSERT INTO public.list (id, title, page_url, type, image_url, wikipedias_by_languages, titles_by_languages, parent_page_url, parent_id)
VALUES (212, 'Ba2', 'Ba2_url', '3rd', null, '{"en": "Ba2_en_url", "ru": "Ba2_ru_url"}', '{"en": "Ba2_en", "ru": "Ba2_ru"}', 'Ba_url', 21);

INSERT INTO public.list (id, title, page_url, type, image_url, wikipedias_by_languages, titles_by_languages, parent_page_url, parent_id)
VALUES (211, 'Ba1', 'Ba1_url', '3rd', null, '{"en": "Ba1_en_url", "ru": "Ba1_ru_url"}', '{"en": "Ba1_en MyWord", "ru": "Ba1_ru MyWord"}', 'Ba_url', 21);

INSERT INTO public.list (id, title, page_url, type, image_url, wikipedias_by_languages, titles_by_languages, parent_page_url, parent_id)
VALUES (221, 'Bb1', 'Bb1_url', '3rd', null, '{"en": "Bb1_en_url", "ru": "Bb1_ru_url"}', '{"en": "Bb1_en", "ru": "Bb1_ru"}', 'Bb_url', 22);

INSERT INTO public.list (id, title, page_url, type, image_url, wikipedias_by_languages, titles_by_languages, parent_page_url, parent_id)
VALUES (222, 'Bb2_en_only', 'Bb2_url', '3rd', null, '{"en": "Bb2_en_url"}', '{"en": "Bb2_en_only MyWord"}', 'Bb_url', 22);

INSERT INTO public.list (id, title, page_url, type, image_url, wikipedias_by_languages, titles_by_languages, parent_page_url, parent_id)
VALUES (2201, 'Bbx1', 'Bbx1_url', '4th', null, '{"en": "Bbx1_en_url", "ru": "Bbx1_ru_url"}', '{"en": "Bbx1_en", "ru": "Bbx1_ru"}', 'Bb_url', 22);

INSERT INTO public.list (id, title, page_url, type, image_url, wikipedias_by_languages, titles_by_languages, parent_page_url, parent_id)
VALUES (2222, 'Bb22', 'Bb22_url', '4th', null, '{"en": "Bb22_en_url", "ru": "Bb22_ru_url"}', '{"en": "Bb22_en", "ru": "Bb22_ru MyWord"}', 'Bb2_url', 222);

INSERT INTO public.list (id, title, page_url, type, image_url, wikipedias_by_languages, titles_by_languages, parent_page_url, parent_id)
VALUES (2221, 'Bb21', 'Bb21_url', '4th', null, '{"en": "Bb21_en_url", "ru": "Bb21_ru_url"}', '{"en": "Bb21_en", "ru": "Bb21_ru"}', 'Bb2_url', 222);

INSERT INTO public.list (id, title, page_url, type, image_url, wikipedias_by_languages, titles_by_languages, parent_page_url, parent_id)
VALUES (22001, 'Bbxx1', 'Bbxx1_url', '5th', null, '{"en": "Bbxx1_en_url", "ru": "Bbxx1_ru_url"}', '{"en": "Bbxx1_en", "ru": "Bbxx1_ru"}', 'Bb_url', 22);

INSERT INTO public.list (id, title, page_url, type, image_url, wikipedias_by_languages, titles_by_languages, parent_page_url, parent_id)
VALUES (11102, 'Aa1x2', 'Aa1x2_url', '5th', null, '{"en": "Aa1x2_en_url", "ru": "Aa1x2_ru_url"}', '{"en": "Aa1x2_en", "ru": "Aa1x2_ru"}', 'Aa1_url', 111);

INSERT INTO public.list (id, title, page_url, type, image_url, wikipedias_by_languages, titles_by_languages, parent_page_url, parent_id)
VALUES (11101, 'Aa1x1', 'Aa1x1_url', '5th', null, '{"en": "Aa1x1_en_url", "ru": "Aa1x1_ru_url"}', '{"en": "Aa1x1_en", "ru": "Aa1x1_ru"}', 'Aa1_url', 111);

INSERT INTO public.list (id, title, page_url, type, image_url, wikipedias_by_languages, titles_by_languages, parent_page_url, parent_id)
VALUES (22201, 'Bb2x1', 'Bb2x1_url', '5th', null, '{"en": "Bb2x1_en_url", "ru": "Bb2x1_ru_url"}', '{"en": "Bb2x1_en", "ru": "Bb2x1_ru"}', 'Bb2_url', 222);

INSERT INTO public.list (id, title, page_url, type, image_url, wikipedias_by_languages, titles_by_languages, parent_page_url, parent_id)
VALUES (22202, 'Bb2x2', 'Bb2x2_url', '5th', null, '{"en": "Bb2x2_en_url", "ru": "Bb2x2_ru_url"}', '{"en": "Bb2x2_en", "ru": "Bb2x2_ru"}', 'Bb2_url', 222);

INSERT INTO public.list (id, title, page_url, type, image_url, wikipedias_by_languages, titles_by_languages, parent_page_url, parent_id)
VALUES (22221, 'Bb221', 'Bb221_url', '5th', null, '{"en": "Bb221_en_url", "ru": "Bb221_ru_url"}', '{"en": "Bb221_en", "ru": "Bb221_ru MyWord"}', 'Bb22_url', 2222);
