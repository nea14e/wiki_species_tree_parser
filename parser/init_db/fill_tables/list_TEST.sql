-- noinspection SqlWithoutWhere
DELETE FROM public.tips_of_the_day;  -- foreign key prevents deletion
-- noinspection SqlWithoutWhere
DELETE FROM public.list;

INSERT INTO public.list (id, title, page_url, type, image_url, wikipedias_by_languages, titles_by_languages, parent_page_url, parent_id, leaves_count)
VALUES (1, 'A', 'A_url', '1st', 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Diversidad_procariota.PNG/265px-Diversidad_procariota.PNG', '{"en": "A_en_url", "ru": "A_ru_url"}', '{"en": "A_en", "ru": "A_ru"}', null, null, 5);

INSERT INTO public.list (id, title, page_url, type, image_url, wikipedias_by_languages, titles_by_languages, parent_page_url, parent_id, leaves_count)
VALUES (2, 'B', 'B_url', '1st', 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/Endomembrane_system_diagram_ru.svg/350px-Endomembrane_system_diagram_ru.svg.png', '{"en": "B_en_url", "ru": "B_ru_url"}', '{"en": "B_en", "ru": "B_ru"}', null, null, 9);

INSERT INTO public.list (id, title, page_url, type, image_url, wikipedias_by_languages, titles_by_languages, parent_page_url, parent_id, leaves_count)
VALUES (3, 'xc', 'xc_url', '2nd', 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Rotavirus_Reconstruction.jpg/275px-Rotavirus_Reconstruction.jpg', '{"en": "xc_en_url", "ru": "xc_ru_url"}', '{"en": "xc_en", "ru": "xc_ru"}', null, null, 1);

INSERT INTO public.list (id, title, page_url, type, image_url, wikipedias_by_languages, titles_by_languages, parent_page_url, parent_id, leaves_count)
VALUES (11, 'Aa', 'Aa_url', '2nd', 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/RedcrestedTuraco.jpg/275px-RedcrestedTuraco.jpg', '{"en": "Aa_en_url", "ru": "Aa_ru_url"}', '{"en": "Aa_en", "ru": "Aa_ru"}', 'A_url', 1, 3);

INSERT INTO public.list (id, title, page_url, type, image_url, wikipedias_by_languages, titles_by_languages, parent_page_url, parent_id, leaves_count)
VALUES (12, 'Ab', 'Ab_url', '2nd', 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/bf/Bird_Diversity_2013.png/275px-Bird_Diversity_2013.png', '{"en": "Ab_en_url", "ru": "Ab_ru_url"}', '{"en": "Ab_en", "ru": "Ab_ru"}', 'A_url', 1, 2);

INSERT INTO public.list (id, title, page_url, type, image_url, wikipedias_by_languages, titles_by_languages, parent_page_url, parent_id, leaves_count)
VALUES (21, 'Ba', 'Ba_url', '2nd', 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/2c/Extant_reptilia.jpg/275px-Extant_reptilia.jpg', '{"en": "Ba_en_url", "ru": "Ba_ru_url"}', '{"en": "Ba_en", "ru": "Ba_ru"}', 'B_url', 2, 2);

INSERT INTO public.list (id, title, page_url, type, image_url, wikipedias_by_languages, titles_by_languages, parent_page_url, parent_id, leaves_count)
VALUES (22, 'Bb_without_languages', 'Bb_url', '2nd', 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Mammal_Diversity_2011.png/275px-Mammal_Diversity_2011.png', '{}', '{}', 'B_url', 2, 7);

INSERT INTO public.list (id, title, page_url, type, image_url, wikipedias_by_languages, titles_by_languages, parent_page_url, parent_id, leaves_count)
VALUES (31, 'xc1', 'xc1_url', '3rd', 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/75/Rana_esculenta_on_Nymphaea_edit.JPG/275px-Rana_esculenta_on_Nymphaea_edit.JPG', '{"en": "xc1_en_url", "ru": "xc1_ru_url"}', '{"en": "xc1_en", "ru": "xc1_ru"}', 'xc_url', 3, 0);

INSERT INTO public.list (id, title, page_url, type, image_url, wikipedias_by_languages, titles_by_languages, parent_page_url, parent_id, leaves_count)
VALUES (111, 'Aa1', 'Aa1_url', '3rd', 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/Afrikanischer_Elefant%2C_Miami.jpg/275px-Afrikanischer_Elefant%2C_Miami.jpg', '{"en": "Aa1_en_url", "ru": "Aa1_ru_url"}', '{"en": "Aa1_en", "ru": "Aa1_ru"}', 'Aa_url', 11, 2);

INSERT INTO public.list (id, title, page_url, type, image_url, wikipedias_by_languages, titles_by_languages, parent_page_url, parent_id, leaves_count)
VALUES (112, 'Aa2', 'Aa2_url', '3rd', 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Tuatara.jpg/275px-Tuatara.jpg', '{"en": "Aa2_en_url", "ru": "Aa2_ru_url"}', '{"en": "Aa2_en", "ru": "Aa2_ru"}', 'Aa_url', 11, 0);

INSERT INTO public.list (id, title, page_url, type, image_url, wikipedias_by_languages, titles_by_languages, parent_page_url, parent_id, leaves_count)
VALUES (121, 'Ab1', 'Ab1_url', '3rd', 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Turtles-Tortoises-Terrapins.jpg/275px-Turtles-Tortoises-Terrapins.jpg', '{"en": "Ab1_en_url", "ru": "Ab1_ru_url"}', '{"en": "Ab1_en", "ru": "Ab1_ru"}', 'Ab_url', 12, 0);

INSERT INTO public.list (id, title, page_url, type, image_url, wikipedias_by_languages, titles_by_languages, parent_page_url, parent_id, leaves_count)
VALUES (122, 'Ab2', 'Ab2_url', '3rd', 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/Musky-rat_%28Hypsiprymnodon_moschatus%29.jpg/275px-Musky-rat_%28Hypsiprymnodon_moschatus%29.jpg', '{"en": "Ab2_en_url", "ru": "Ab2_ru_url"}', '{"en": "Ab2_en", "ru": "Ab2_ru"}', 'Ab_url', 12, 0);

INSERT INTO public.list (id, title, page_url, type, image_url, wikipedias_by_languages, titles_by_languages, parent_page_url, parent_id, leaves_count)
VALUES (211, 'Ba1', 'Ba1_url', '3rd', 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Carnivora_portraits.jpg/213px-Carnivora_portraits.jpg', '{"en": "Ba1_en_url", "ru": "Ba1_ru_url"}', '{"en": "Ba1_en", "ru": "Ba1_ru"}', 'Ba_url', 21, 0);

INSERT INTO public.list (id, title, page_url, type, image_url, wikipedias_by_languages, titles_by_languages, parent_page_url, parent_id, leaves_count)
VALUES (212, 'Ba2', 'Ba2_url', '3rd', 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/Eulipotyphla.jpg/275px-Eulipotyphla.jpg', '{"en": "Ba2_en_url", "ru": "Ba2_ru_url"}', '{"en": "Ba2_en", "ru": "Ba2_ru"}', 'Ba_url', 21, 0);

INSERT INTO public.list (id, title, page_url, type, image_url, wikipedias_by_languages, titles_by_languages, parent_page_url, parent_id, leaves_count)
VALUES (221, 'Bb1', 'Bb1_url', '3rd', 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/The_Artiodactyla.jpg/275px-The_Artiodactyla.jpg', '{"en": "Bb1_en_url", "ru": "Bb1_ru_url"}', '{"en": "Bb1_en", "ru": "Bb1_ru"}', 'Bb_url', 22, 0);

INSERT INTO public.list (id, title, page_url, type, image_url, wikipedias_by_languages, titles_by_languages, parent_page_url, parent_id, leaves_count)
VALUES (222, 'Bb2_en_only', 'Bb2_url', '3rd', 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/White_Rhino.jpg/275px-White_Rhino.jpg', '{"en": "Bb2_en_url"}', '{"en": "Bb2_en_only"}', 'Bb_url', 22, 4);

INSERT INTO public.list (id, title, page_url, type, image_url, wikipedias_by_languages, titles_by_languages, parent_page_url, parent_id, leaves_count)
VALUES (2201, 'Bbx1', 'Bbx1_url', '4th', 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/Equus_quagga_burchellii_-_Etosha%2C_2014.jpg/275px-Equus_quagga_burchellii_-_Etosha%2C_2014.jpg', '{"en": "Bbx1_en_url", "ru": "Bbx1_ru_url"}', '{"en": "Bbx1_en", "ru": "Bbx1_ru"}', 'Bb_url', 22, 0);

INSERT INTO public.list (id, title, page_url, type, image_url, wikipedias_by_languages, titles_by_languages, parent_page_url, parent_id, leaves_count)
VALUES (2221, 'Bb21', 'Bb21_url', '4th', 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Waterberg_Nashorn2.jpg/275px-Waterberg_Nashorn2.jpg', '{"en": "Bb21_en_url", "ru": "Bb21_ru_url"}', '{"en": "Bb21_en", "ru": "Bb21_ru"}', 'Bb2_url', 222, 0);

INSERT INTO public.list (id, title, page_url, type, image_url, wikipedias_by_languages, titles_by_languages, parent_page_url, parent_id, leaves_count)
VALUES (2222, 'Bb22', 'Bb22_url', '4th', 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/Tapirus_terrestris.jpg/275px-Tapirus_terrestris.jpg', '{"en": "Bb22_en_url", "ru": "Bb22_ru_url"}', '{"en": "Bb22_en", "ru": "Bb22_ru"}', 'Bb2_url', 222, 1);

INSERT INTO public.list (id, title, page_url, type, image_url, wikipedias_by_languages, titles_by_languages, parent_page_url, parent_id, leaves_count)
VALUES (11101, 'Aa1x1', 'Aa1x1_url', '5th', 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/42/Galapagos_giant_tortoise_Geochelone_elephantopus.jpg/275px-Galapagos_giant_tortoise_Geochelone_elephantopus.jpg', '{"en": "Aa1x1_en_url", "ru": "Aa1x1_ru_url"}', '{"en": "Aa1x1_en", "ru": "Aa1x1_ru"}', 'Aa1_url', 111, 0);

INSERT INTO public.list (id, title, page_url, type, image_url, wikipedias_by_languages, titles_by_languages, parent_page_url, parent_id, leaves_count)
VALUES (11102, 'Aa1x2', 'Aa1x2_url', '5th', 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/bb/Hawaii_turtle_2.JPG/275px-Hawaii_turtle_2.JPG', '{"en": "Aa1x2_en_url", "ru": "Aa1x2_ru_url"}', '{"en": "Aa1x2_en", "ru": "Aa1x2_ru"}', 'Aa1_url', 111, 0);

INSERT INTO public.list (id, title, page_url, type, image_url, wikipedias_by_languages, titles_by_languages, parent_page_url, parent_id, leaves_count)
VALUES (22001, 'Bbxx1', 'Bbxx1_url', '5th', 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/2004_04_18_Trachemys_2.jpg/275px-2004_04_18_Trachemys_2.jpg', '{"en": "Bbxx1_en_url", "ru": "Bbxx1_ru_url"}', '{"en": "Bbxx1_en", "ru": "Bbxx1_ru"}', 'Bb_url', 22, 0);

INSERT INTO public.list (id, title, page_url, type, image_url, wikipedias_by_languages, titles_by_languages, parent_page_url, parent_id, leaves_count)
VALUES (22201, 'Bb2x1', 'Bb2x1_url', '5th', 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Testudo_graeca11.JPG/275px-Testudo_graeca11.JPG', '{"en": "Bb2x1_en_url", "ru": "Bb2x1_ru_url"}', '{"en": "Bb2x1_en", "ru": "Bb2x1_ru"}', 'Bb2_url', 222, 0);

INSERT INTO public.list (id, title, page_url, type, image_url, wikipedias_by_languages, titles_by_languages, parent_page_url, parent_id, leaves_count)
VALUES (22202, 'Bb2x2', 'Bb2x2_url', '5th', 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/Leatherback_sea_turtle_Tinglar%2C_USVI_%285839996547%29.jpg/275px-Leatherback_sea_turtle_Tinglar%2C_USVI_%285839996547%29.jpg', '{"en": "Bb2x2_en_url", "ru": "Bb2x2_ru_url"}', '{"en": "Bb2x2_en", "ru": "Bb2x2_ru"}', 'Bb2_url', 222, 0);

INSERT INTO public.list (id, title, page_url, type, image_url, wikipedias_by_languages, titles_by_languages, parent_page_url, parent_id, leaves_count)
VALUES (22221, 'Bb221', 'Bb221_url', '5th', 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Alligator_snapping_turtle_-_Geierschildkr%C3%B6te_-_Alligatorschildkr%C3%B6te_-_Macrochelys_temminckii_01.jpg/275px-Alligator_snapping_turtle_-_Geierschildkr%C3%B6te_-_Alligatorschildkr%C3%B6te_-_Macrochelys_temminckii_01.jpg', '{"en": "Bb221_en_url", "ru": "Bb221_ru_url"}', '{"en": "Bb221_en", "ru": "Bb221_ru"}', 'Bb22_url', 2222, 0);
