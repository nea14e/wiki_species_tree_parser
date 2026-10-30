-- noinspection SqlWithoutWhere
DELETE FROM public.changed_tips;  -- foreign key prevents deletion
-- noinspection SqlWithoutWhere
DELETE FROM public.tips_of_the_day;  -- foreign key prevents deletion
-- noinspection SqlWithoutWhere
DELETE FROM public.list;

INSERT INTO public.list (id, title, page_id, type, image_url, titles_by_languages, parent_title, parent_id, leaves_count, last_error_message, latin)
VALUES (1, 'A', 'A_url', '1st', '//thumb.wikimedia.org/wikipedia/commons/thumb/b/b2/Baikal_Seal_in_the_Irkutsk_Aquarium_%28September_2025%29_-_0_2.jpg/330px-Baikal_Seal_in_the_Irkutsk_Aquarium_%28September_2025%29_-_0_2.jpg?utm_source=ru.wikipedia.org&utm_campaign=parser&utm_content=thumbnail', '{"en": "A_en", "ru": "A_ru"}', null, null, 5, null, 'A_latin');

INSERT INTO public.list (id, title, page_id, type, image_url, titles_by_languages, parent_title, parent_id, leaves_count, last_error_message, latin)
VALUES (2, 'B', 'B_url', '1st', '//thumb.wikimedia.org/wikipedia/commons/thumb/8/80/1966_CPA_3402.jpg/330px-1966_CPA_3402.jpg?utm_source=ru.wikipedia.org&utm_campaign=parser&utm_content=thumbnail', '{"en": "B_en", "ru": "B_ru"}', null, null, 13, null, 'B_latin');

INSERT INTO public.list (id, title, page_id, type, image_url, titles_by_languages, parent_title, parent_id, leaves_count, last_error_message, latin)
VALUES (3, 'xc', 'xc_url', '2nd', '//thumb.wikimedia.org/wikipedia/commons/thumb/8/80/Cassin%27s_auklet_2.JPG/330px-Cassin%27s_auklet_2.JPG?utm_source=ru.wikipedia.org&utm_campaign=parser&utm_content=thumbnail', '{"en": "xc_en", "ru": "xc_ru"}', null, null, 1, null, 'xc_latin');

INSERT INTO public.list (id, title, page_id, type, image_url, titles_by_languages, parent_title, parent_id, leaves_count, last_error_message, latin)
VALUES (11, 'Aa', 'Aa_url', '2nd', '//thumb.wikimedia.org/wikipedia/commons/thumb/9/97/Abdarainurus.jpg/330px-Abdarainurus.jpg?utm_source=ru.wikipedia.org&utm_campaign=parser&utm_content=thumbnail', '{"en": "Aa_en", "ru": "Aa_ru"}', 'A_url', 1, 3, null, 'Aa_latin');

INSERT INTO public.list (id, title, page_id, type, image_url, titles_by_languages, parent_title, parent_id, leaves_count, last_error_message, latin)
VALUES (12, 'Ab', 'Ab_url', '2nd', '//thumb.wikimedia.org/wikipedia/commons/thumb/4/49/Abdera_flexuosa_up.jpg/330px-Abdera_flexuosa_up.jpg?utm_source=ru.wikipedia.org&utm_campaign=parser&utm_content=thumbnail', '{"en": "Ab_en", "ru": "Ab_ru"}', 'A_url', 1, 2, null, 'Ab_latin');

INSERT INTO public.list (id, title, page_id, type, image_url, titles_by_languages, parent_title, parent_id, leaves_count, last_error_message, latin)
VALUES (21, 'Ba', 'Ba_url', '2nd', '//upload.wikimedia.org/wikipedia/commons/6/62/Marsh_fly01.jpg?utm_source=ru.wikipedia.org&utm_campaign=parser&utm_content=thumbnail_unscaled', '{"en": "Ba_en", "ru": "Ba_ru"}', 'B_url', 2, 2, null, 'Ba_latin');

INSERT INTO public.list (id, title, page_id, type, image_url, titles_by_languages, parent_title, parent_id, leaves_count, last_error_message, latin)
VALUES (22, 'Bb_without_languages', 'Bb_url', '2nd', '//thumb.wikimedia.org/wikipedia/commons/thumb/5/52/Acanthacorydalis_asiatica.jpg/330px-Acanthacorydalis_asiatica.jpg?utm_source=ru.wikipedia.org&utm_campaign=parser&utm_content=thumbnail', '{}', 'B_url', 2, 9, null, 'Bb_without_languages_latin');

INSERT INTO public.list (id, title, page_id, type, image_url, titles_by_languages, parent_title, parent_id, leaves_count, last_error_message, latin)
VALUES (23, 'Bc_en_only', 'Bc_en_only_url', '2nd', '//thumb.wikimedia.org/wikipedia/commons/thumb/3/37/Garden_locust_%28Acanthacris_ruficornis%29.jpg/330px-Garden_locust_%28Acanthacris_ruficornis%29.jpg?utm_source=ru.wikipedia.org&utm_campaign=parser&utm_content=thumbnail', '{"en": "Bc_en"}', 'B_url', 2, 0, null, 'Bc_en_only_latin');

INSERT INTO public.list (id, title, page_id, type, image_url, titles_by_languages, parent_title, parent_id, leaves_count, last_error_message, latin)
VALUES (24, 'Bd_ru_only', 'Bd_ru_only_url', '2nd', '//thumb.wikimedia.org/wikipedia/commons/thumb/c/cf/UplandSandpiperOntarioCropped.jpg/330px-UplandSandpiperOntarioCropped.jpg?utm_source=ru.wikipedia.org&utm_campaign=parser&utm_content=thumbnail', '{"ru": "Bd_ru"}', 'B_url', 2, 0, null, 'Bd_ru_only_latin');

INSERT INTO public.list (id, title, page_id, type, image_url, titles_by_languages, parent_title, parent_id, leaves_count, last_error_message, latin)
VALUES (31, 'xc1', 'xc1_url', '3rd', '//thumb.wikimedia.org/wikipedia/commons/thumb/5/57/Marmotte-bobak.png/330px-Marmotte-bobak.png?utm_source=ru.wikipedia.org&utm_campaign=parser&utm_content=thumbnail', '{"en": "xc1_en", "ru": "xc1_ru"}', 'xc_url', 3, 0, null, 'xc1_latin');

INSERT INTO public.list (id, title, page_id, type, image_url, titles_by_languages, parent_title, parent_id, leaves_count, last_error_message, latin)
VALUES (111, 'Aa1', 'Aa1_url', '3rd', '//thumb.wikimedia.org/wikipedia/commons/thumb/c/cd/Hirscheber1a.jpg/330px-Hirscheber1a.jpg?utm_source=ru.wikipedia.org&utm_campaign=parser&utm_content=thumbnail', '{"en": "Aa1_en", "ru": "Aa1_ru"}', 'Aa_url', 11, 2, null, 'Aa1_latin');

INSERT INTO public.list (id, title, page_id, type, image_url, titles_by_languages, parent_title, parent_id, leaves_count, last_error_message, latin)
VALUES (112, 'Aa2', 'Aa2_url', '3rd', '//thumb.wikimedia.org/wikipedia/commons/thumb/f/f2/CorduliaAeneaMale.jpg/330px-CorduliaAeneaMale.jpg?utm_source=ru.wikipedia.org&utm_campaign=parser&utm_content=thumbnail', '{"en": "Aa2_en", "ru": "Aa2_ru"}', 'Aa_url', 11, 0, null, 'Aa2_latin');

INSERT INTO public.list (id, title, page_id, type, image_url, titles_by_languages, parent_title, parent_id, leaves_count, last_error_message, latin)
VALUES (121, 'Ab1', 'Ab1_url', '3rd', '//thumb.wikimedia.org/wikipedia/commons/thumb/3/30/Heterogenea_asella_-_The_Triangle_-_%D0%91%D0%B0%D0%B1%D0%BE%D1%87%D0%BA%D0%B0-%D0%BE%D1%81%D0%BB%D0%B8%D0%BA_%2841008419861%29.jpg/330px-Heterogenea_asella_-_The_Triangle_-_%D0%91%D0%B0%D0%B1%D0%BE%D1%87%D0%BA%D0%B0-%D0%BE%D1%81%D0%BB%D0%B8%D0%BA_%2841008419861%29.jpg?utm_source=ru.wikipedia.org&utm_campaign=parser&utm_content=thumbnail', '{"en": "Ab1_en", "ru": "Ab1_ru"}', 'Ab_url', 12, 0, null, 'Ab1_latin');

INSERT INTO public.list (id, title, page_id, type, image_url, titles_by_languages, parent_title, parent_id, leaves_count, last_error_message, latin)
VALUES (122, 'Ab2', 'Ab2_url', '3rd', '//thumb.wikimedia.org/wikipedia/commons/thumb/1/1d/Kleinfluegler-Mallorca-01.jpg/330px-Kleinfluegler-Mallorca-01.jpg?utm_source=ru.wikipedia.org&utm_campaign=parser&utm_content=thumbnail', '{"en": "Ab2_en", "ru": "Ab2_ru"}', 'Ab_url', 12, 0, null, 'Ab2_latin');

INSERT INTO public.list (id, title, page_id, type, image_url, titles_by_languages, parent_title, parent_id, leaves_count, last_error_message, latin)
VALUES (211, 'Ba1', 'Ba1_url', '3rd', '//thumb.wikimedia.org/wikipedia/commons/thumb/4/48/Dwarf_Fat-tailed_Mouse_Opossum_imported_from_iNaturalist_photo_351995812_on_19_October_2024.jpg/330px-Dwarf_Fat-tailed_Mouse_Opossum_imported_from_iNaturalist_photo_351995812_on_19_October_2024.jpg?utm_source=ru.wikipedia.org&utm_campaign=parser&utm_content=thumbnail', '{"en": "Ba1_en", "ru": "Ba1_ru"}', 'Ba_url', 21, 0, null, 'Ba1_latin');

INSERT INTO public.list (id, title, page_id, type, image_url, titles_by_languages, parent_title, parent_id, leaves_count, last_error_message, latin)
VALUES (212, 'Ba2', 'Ba2_url', '3rd', '//thumb.wikimedia.org/wikipedia/commons/thumb/1/1e/Black-faced_Warbler_Naina_Devi_Himalayan_Bird_Conservation_Reserve_Nainital_Uttarakhand_India_28.11.2015.jpg/330px-Black-faced_Warbler_Naina_Devi_Himalayan_Bird_Conservation_Reserve_Nainital_Uttarakhand_India_28.11.2015.jpg?utm_source=ru.wikipedia.org&utm_campaign=parser&utm_content=thumbnail', '{"en": "Ba2_en", "ru": "Ba2_ru"}', 'Ba_url', 21, 0, null, 'Ba2_latin');

INSERT INTO public.list (id, title, page_id, type, image_url, titles_by_languages, parent_title, parent_id, leaves_count, last_error_message, latin)
VALUES (221, 'Bb1', 'Bb1_url', '3rd', '//thumb.wikimedia.org/wikipedia/commons/thumb/2/2b/Abryna_regispetri_%2815653307343%29.jpg/330px-Abryna_regispetri_%2815653307343%29.jpg?utm_source=ru.wikipedia.org&utm_campaign=parser&utm_content=thumbnail', '{"en": "Bb1_en", "ru": "Bb1_ru"}', 'Bb_url', 22, 0, null, 'Bb1_latin');

INSERT INTO public.list (id, title, page_id, type, image_url, titles_by_languages, parent_title, parent_id, leaves_count, last_error_message, latin)
VALUES (222, 'Bb2_en_only', 'Bb2_url', '3rd', '//thumb.wikimedia.org/wikipedia/commons/thumb/3/3e/Insect_Firefly_%28Lampyridae%29_from_Ezhimala_DSCN1755.jpg/330px-Insect_Firefly_%28Lampyridae%29_from_Ezhimala_DSCN1755.jpg?utm_source=ru.wikipedia.org&utm_campaign=parser&utm_content=thumbnail', '{"en": "Bb2_en_only"}', 'Bb_url', 22, 4, null, 'Bb2_en_only_latin');

INSERT INTO public.list (id, title, page_id, type, image_url, titles_by_languages, parent_title, parent_id, leaves_count, last_error_message, latin)
VALUES (223, 'Bb3', 'Bb3_url', '3rd', '//thumb.wikimedia.org/wikipedia/commons/thumb/d/de/Papio_cynocephalus02.jpg/250px-Papio_cynocephalus02.jpg?utm_source=ru.wikipedia.org&utm_campaign=parser&utm_content=thumbnail', '{"en": "Bb3_en", "ru": "Bb3_ru"}', 'Bb_url', 22, 0, null, 'Bb3_latin');

INSERT INTO public.list (id, title, page_id, type, image_url, titles_by_languages, parent_title, parent_id, leaves_count, last_error_message, latin)
VALUES (224, 'Bb4', 'Bb4_url', '3rd', '//thumb.wikimedia.org/wikipedia/commons/thumb/1/12/Bathyporeia_elegans.jpg/330px-Bathyporeia_elegans.jpg?utm_source=ru.wikipedia.org&utm_campaign=parser&utm_content=thumbnail', '{"en": "Bb4_en", "ru": "Bb4_ru"}', 'Bb_url', 22, 0, null, 'Bb4_latin');

INSERT INTO public.list (id, title, page_id, type, image_url, titles_by_languages, parent_title, parent_id, leaves_count, last_error_message, latin)
VALUES (2201, 'Bbx1', 'Bbx1_url', '4th', '//thumb.wikimedia.org/wikipedia/commons/thumb/8/8e/Agouti_%28PSF%29.png/330px-Agouti_%28PSF%29.png?utm_source=ru.wikipedia.org&utm_campaign=parser&utm_content=thumbnail', '{"en": "Bbx1_en", "ru": "Bbx1_ru"}', 'Bb_url', 22, 0, null, 'Bbx1_latin');

INSERT INTO public.list (id, title, page_id, type, image_url, titles_by_languages, parent_title, parent_id, leaves_count, last_error_message, latin)
VALUES (2221, 'Bb21', 'Bb21_url', '4th', '//thumb.wikimedia.org/wikipedia/commons/thumb/4/4e/Abzaria_latipetiolaris.png/330px-Abzaria_latipetiolaris.png?utm_source=ru.wikipedia.org&utm_campaign=parser&utm_content=thumbnail', '{"en": "Bb21_en", "ru": "Bb21_ru"}', 'Bb2_url', 222, 0, null, 'Bb21_latin');

INSERT INTO public.list (id, title, page_id, type, image_url, titles_by_languages, parent_title, parent_id, leaves_count, last_error_message, latin)
VALUES (2222, 'Bb22', 'Bb22_url', '4th', '//thumb.wikimedia.org/wikipedia/commons/thumb/3/37/Feuerweber_Zoo_Berlin_3.jpg/250px-Feuerweber_Zoo_Berlin_3.jpg?utm_source=ru.wikipedia.org&utm_campaign=parser&utm_content=thumbnail', '{"en": "Bb22_en", "ru": "Bb22_ru"}', 'Bb2_url', 222, 1, null, 'Bb22_latin');

INSERT INTO public.list (id, title, page_id, type, image_url, titles_by_languages, parent_title, parent_id, leaves_count, last_error_message, latin)
VALUES (11101, 'Aa1x1', 'Aa1x1_url', '5th', '//thumb.wikimedia.org/wikipedia/commons/thumb/1/14/Bavarianpinevole.jpg/330px-Bavarianpinevole.jpg?utm_source=ru.wikipedia.org&utm_campaign=parser&utm_content=thumbnail', '{"en": "Aa1x1_en", "ru": "Aa1x1_ru"}', 'Aa1_url', 111, 0, null, 'Aa1x1_latin');

INSERT INTO public.list (id, title, page_id, type, image_url, titles_by_languages, parent_title, parent_id, leaves_count, last_error_message, latin)
VALUES (11102, 'Aa1x2', 'Aa1x2_url', '5th', '//thumb.wikimedia.org/wikipedia/commons/thumb/f/f1/Spindalis_zena_pretrei%2C_Ciego_de_Avila_Province%2C_Cuba_1_%28cropped%29.jpg/330px-Spindalis_zena_pretrei%2C_Ciego_de_Avila_Province%2C_Cuba_1_%28cropped%29.jpg?utm_source=ru.wikipedia.org&utm_campaign=parser&utm_content=thumbnail', '{"en": "Aa1x2_en", "ru": "Aa1x2_ru"}', 'Aa1_url', 111, 0, null, 'Aa1x2_latin');

INSERT INTO public.list (id, title, page_id, type, image_url, titles_by_languages, parent_title, parent_id, leaves_count, last_error_message, latin)
VALUES (22001, 'Bbxx1', 'Bbxx1_url', '5th', '//thumb.wikimedia.org/wikipedia/commons/thumb/c/cc/AbacoIsBoa.JPG/330px-AbacoIsBoa.JPG?utm_source=ru.wikipedia.org&utm_campaign=parser&utm_content=thumbnail', '{"en": "Bbxx1_en", "ru": "Bbxx1_ru"}', 'Bb_url', 22, 0, null, 'Bbxx1_latin');

INSERT INTO public.list (id, title, page_id, type, image_url, titles_by_languages, parent_title, parent_id, leaves_count, last_error_message, latin)
VALUES (22201, 'Bb2x1', 'Bb2x1_url', '5th', '//thumb.wikimedia.org/wikipedia/commons/thumb/c/c0/Dendroica_bachmanii_%28cropped%29.jpg/330px-Dendroica_bachmanii_%28cropped%29.jpg?utm_source=ru.wikipedia.org&utm_campaign=parser&utm_content=thumbnail', '{"en": "Bb2x1_en", "ru": "Bb2x1_ru"}', 'Bb2_url', 222, 0, null, 'Bb2x1_latin');

INSERT INTO public.list (id, title, page_id, type, image_url, titles_by_languages, parent_title, parent_id, leaves_count, last_error_message, latin)
VALUES (22202, 'Bb2x2', 'Bb2x2_url', '5th', '//thumb.wikimedia.org/wikipedia/commons/thumb/3/30/Bagarius_yarrellii_Mintern_115.jpg/330px-Bagarius_yarrellii_Mintern_115.jpg?utm_source=ru.wikipedia.org&utm_campaign=parser&utm_content=thumbnail', '{"en": "Bb2x2_en", "ru": "Bb2x2_ru"}', 'Bb2_url', 222, 0, null, 'Bb2x2_latin');

INSERT INTO public.list (id, title, page_id, type, image_url, titles_by_languages, parent_title, parent_id, leaves_count, last_error_message, latin)
VALUES (22221, 'Bb221', 'Bb221_url', '5th', '//thumb.wikimedia.org/wikipedia/commons/thumb/4/41/Spongillidae.full.length.jpg/330px-Spongillidae.full.length.jpg?utm_source=ru.wikipedia.org&utm_campaign=parser&utm_content=thumbnail', '{"en": "Bb221_en", "ru": "Bb221_ru"}', 'Bb22_url', 2222, 0, null, 'Bb221_latin');
