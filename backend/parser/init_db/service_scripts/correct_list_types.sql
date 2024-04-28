UPDATE public.list
SET type = trim(type)
WHERE type LIKE ' %'
  OR type LIKE '% ';

UPDATE public.list
SET type = replace(type, chr(9), '')
WHERE type LIKE (chr(9) || '%');

UPDATE public.list
SET type = replace(type, 'Super', 'Supra')
WHERE type ILIKE 'Super%';



SELECT type, count(1)
FROM public.list
WHERE type NOT IN (SELECT ranks.type
                   FROM public.ranks)
GROUP BY type
ORDER BY count(1) DESC;