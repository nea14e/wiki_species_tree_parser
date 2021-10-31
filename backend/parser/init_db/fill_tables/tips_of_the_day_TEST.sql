WITH cte(id, tip_on_languages, page_url) AS (
  VALUES (1, '{
                "ru": "Если названия вида на нужном языке нет в базе данных, используется латынь. Также вы можете искать на латыни любые виды.",
                "en": "If the species name in the required language is not in the database, Latin is used. You can also search for any tree node in Latin."
              }'::jsonb, NULL),
         (2, '{
                "ru": "Вы можете перейти к чтению Википедии, нажав на ссылку в любом узле дерева.",
                "en": "You can go to reading Wikipedia by clicking on the link at any node in the tree."
              }'::jsonb, NULL),
         (3, '{
                "ru": "Исключительно русский совет."
              }'::jsonb, NULL),
         (4, '{
                "ru": "Посмотрите, какой интересный вид Bb22!",
                "en": "Let''s see Bb22, it is very interesting species!"
              }'::jsonb, 'Bb22_url'),
         (5, '{
                "ru": "Посмотрите, какой интересный вид Bb2!",
                "en": "Let''s see Bb2, it is very interesting species!"
              }'::jsonb, 'Bb2_url')
),
     upd AS (
       UPDATE public.tips_of_the_day
         SET
           tip_on_languages = cte.tip_on_languages,
           page_url = cte.page_url
         FROM cte
         WHERE tips_of_the_day.id = cte.id
         RETURNING cte.id
     ),
     ins AS (
       INSERT INTO public.tips_of_the_day (id, tip_on_languages, page_url)
         SELECT *
         FROM cte
         WHERE cte.id NOT IN (SELECT id
                              FROM upd)
         RETURNING id
     )
DELETE
FROM public.tips_of_the_day
WHERE id NOT IN (SELECT id
                 FROM upd)
  AND id NOT IN (SELECT id
                 FROM ins);