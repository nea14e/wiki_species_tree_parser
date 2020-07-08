WITH cte(lang_key, comment, site_title,
         site_description,
         parent_word, rank_word, search_word, tip_of_the_day_word, authors_word,
         authors_content) AS (
  VALUES ('ru', 'Русский', 'Дерево видов',
          'Биологическая систематика более чем 100 000 видов животных, растений, бактерий и грибов. Фотографии и информация для построения дерева взяты из проекта Викивиды',
          'Родитель', 'Ранг', 'Поиск', 'Совет дня', 'Авторы',
          'Сделано коллективом добровольцев, в том числе с использованием рабочего времени и ресурсов, щедро предоставленных <a href="https://it-avangard.su/">ООО "ИТ-Авангард"</a>.'),
         ('en', 'English', 'Species tree',
          'Biological systematics of more than 100,000 species of animals, plants, bacteria and fungi. Photos and information for building a tree are taken from the Wikispecies/Wikipedia project',
          'Parent', 'Rank', 'Search', 'Tip of the day', 'Authors',
          'Made by team of volunteers from <a href="https://it-avangard.su/">https://it-avangard.su/</a> company.')
),
     upd AS (
       UPDATE public.known_languages
         SET
           comment = cte.comment,
           site_title = cte.site_title,
           site_description = cte.site_description,
           parent_word = cte.parent_word,
           rank_word = cte.rank_word,
           search_word = cte.search_word,
           tip_of_the_day_word = cte.tip_of_the_day_word,
           authors_word = cte.authors_word,
           authors_content = cte.authors_content
         FROM cte
         WHERE known_languages.lang_key = cte.lang_key
         RETURNING cte.lang_key
     ),
     ins AS (
       INSERT INTO public.known_languages
         SELECT *
         FROM cte
         WHERE cte.lang_key NOT IN (SELECT lang_key
                                    FROM upd)
         RETURNING lang_key
     )
DELETE
FROM public.known_languages
WHERE lang_key NOT IN (SELECT lang_key
                       FROM upd)
  AND lang_key NOT IN (SELECT lang_key
                       FROM ins);