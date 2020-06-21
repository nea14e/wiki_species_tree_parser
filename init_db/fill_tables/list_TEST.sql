-- noinspection SqlWithoutWhere
DELETE FROM public.list;

INSERT INTO public.list(id, title, page_url, type, image_url, wikipedias_by_languages, parent_page_url, parent_id, titles_by_languages)
VALUES
       (1, 'A', 'A_url', '1st', null, '{"ru": "A_ru_url", "en":  "A_en_url"}', null, null, '{"ru": "A_ru", "en":  "A_en"}'),
       (2, 'B', 'B_url', '1st', null, '{"ru": "B_ru_url", "en":  "B_en_url"}', null, null, '{"ru": "B_ru", "en":  "B_en"}'),
       (11, 'Aa', 'Aa_url', '2nd', null, '{"ru": "Aa_ru_url", "en":  "Aa_en_url"}', 'A_url', null, '{"ru": "Aa_ru", "en":  "Aa_en"}'),
       (21, 'Ba', 'Ba_url', '2nd', null, '{"ru": "Ba_ru_url", "en":  "Ba_en_url"}', 'B_url', null, '{"ru": "Ba_ru", "en":  "Ba_en"}'),
       (12, 'Ab', 'Ab_url', '2nd', null, '{"en":  "Ab_en_url"}', 'A_url', null, '{"ru": "Ab_ru", "en":  "Ab_en"}'),
       (22, 'Bb', 'Bb_url', '2nd', null, '{"en":  "Bb_en_url"}', 'B_url', null, '{"ru": "Bb_ru", "en":  "Bb_en"}'),
       (111, 'Aa1', 'Aa1_url', '3rd', null, '{"ru": "Aa1_ru_url", "en":  "Aa1_en_url"}', 'Aa_url', null, '{"ru": "Aa1_ru", "en":  "Aa1_en"}'),
       (211, 'Ba1', 'Ba1_url', '3rd', null, '{"ru": "Ba1_ru_url", "en":  "Ba1_en_url"}', 'Ba_url', null, '{"ru": "Ba1_ru", "en":  "Ba1_en"}'),
       (121, 'Ab1', 'Ab1_url', '3rd', null, '{"ru": "Ab1_ru_url", "en":  "Ab1_en_url"}', 'Ab_url', null, '{"ru": "Ab1_ru", "en":  "Ab1_en"}'),
       (221, 'Bb1', 'Bb1_url', '3rd', null, '{"ru": "Bb1_ru_url", "en":  "Bb1_en_url"}', 'Bb_url', null, '{"ru": "Bb1_ru", "en":  "Bb1_en"}'),
       (112, 'Aa2', 'Aa2_url', '3rd', null, '{"ru": "Aa2_ru_url", "en":  "Aa2_en_url"}', 'Aa_url', null, '{"ru": "Aa2_ru", "en":  "Aa2_en"}'),
       (212, 'Ba2', 'Ba2_url', '3rd', null, '{"ru": "Ba2_ru_url", "en":  "Ba2_en_url"}', 'Ba_url', null, '{"ru": "Ba2_ru", "en":  "Ba2_en"}'),
       (122, 'Ab2', 'Ab2_url', '3rd', null, '{"ru": "Ab2_ru_url", "en":  "Ab2_en_url"}', 'Ab_url', null, '{"ru": "Ab2_ru", "en":  "Ab2_en"}'),
       (222, 'Bb2', 'Bb2_url', '3rd', null, '{"ru": "Bb2_ru_url", "en":  "Bb2_en_url"}', 'Bb_url', null, '{"ru": "Bb2_ru", "en":  "Bb2_en"}'),
       (11101, 'Aa1x1', 'Aa1x1_url', '5th', null, '{"ru": "Aa1x1_ru_url", "en":  "Aa1x1_en_url"}', 'Aa1_url', null, '{"ru": "Aa1x1_ru", "en":  "Aa1x1_en"}'),
       (11102, 'Aa1x2', 'Aa1x2_url', '5th', null, '{"ru": "Aa1x2_ru_url", "en":  "Aa1x2_en_url"}', 'Aa1_url', null, '{"ru": "Aa1x2_ru", "en":  "Aa1x2_en"}'),
       (2221, 'Bb21', 'Bb21_url', '4th', null, '{"ru": "Bb21_ru_url", "en":  "Bb21_en_url"}', 'Bb2_url', null, '{"ru": "Bb21_ru", "en":  "Bb21_en"}'),
       (2222, 'Bb22', 'Bb22_url', '4th', null, '{"ru": "Bb22_ru_url", "en":  "Bb22_en_url"}', 'Bb2_url', null, '{"ru": "Bb22_ru", "en":  "Bb22_en"}'),
       (22201, 'Bb2x1', 'Bb2x1_url', '5th', null, '{"ru": "Bb2x1_ru_url", "en":  "Bb2x1_en_url"}', 'Bb2_url', null, '{"ru": "Bb2x1_ru", "en":  "Bb2x1_en"}'),
       (22202, 'Bb2x2', 'Bb2x2_url', '5th', null, '{"ru": "Bb2x2_ru_url", "en":  "Bb2x2_en_url"}', 'Bb2_url', null, '{"ru": "Bb2x2_ru", "en":  "Bb2x2_en"}');