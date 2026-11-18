WITH cte(id, tip_on_languages, list_id) AS (VALUES (1, '{
  "ru": "Если названия вида на нужном языке нет в базе данных, используется латынь. Также вы можете искать на латыни любые виды.",
  "en": "If the species name in the required language is not in the database, Latin is used. You can also search for any tree node in Latin."
}'::jsonb, NULL),
                                                   (2, '{
                                                     "ru": "Вы можете перейти к чтению Википедии, нажав на ссылку в любом узле дерева.",
                                                     "en": "You can go to reading Wikipedia by clicking on the link at any node in the tree."
                                                   }'::jsonb, NULL),
                                                   (3, '{
                                                     "en": "You can go to reading Wikipedia by clicking on the link at any node in the tree.",
                                                     "ru": "Вы можете перейти к чтению Википедии, нажав на ссылку в любом узле дерева."
                                                   }'::jsonb, 56089)),
     upd AS (
         UPDATE public.tips_of_the_day
             SET
                 tip_on_languages = cte.tip_on_languages,
                 list_id = cte.list_id
             FROM cte
             WHERE tips_of_the_day.id = cte.id
             RETURNING cte.id),
     ins AS (
         INSERT INTO public.tips_of_the_day (id, tip_on_languages, list_id)
             SELECT *
             FROM cte
             WHERE cte.id NOT IN (SELECT id
                                  FROM upd)
             RETURNING id)
DELETE
FROM public.tips_of_the_day
WHERE id NOT IN (SELECT id
                 FROM upd)
  AND id NOT IN (SELECT id
                 FROM ins);