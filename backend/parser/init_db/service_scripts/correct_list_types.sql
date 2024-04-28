-- Spaces:

UPDATE public.list
SET type = trim(type)
WHERE type LIKE ' %'
  OR type LIKE '% ';

-- Tabs:

UPDATE public.list
SET type = replace(type, chr(9), '')
WHERE type LIKE (chr(9) || '%');

-- Super -> Supra:

UPDATE public.list
SET type = replace(type, 'Super', 'Supra')
WHERE type ILIKE 'Super%';

-- Classis:

UPDATE public.list
SET type = replace(type, 'classes', 'classis')
WHERE type LIKE '%classes%';

UPDATE public.list
SET type = replace(type, 'Classes', 'Classis')
WHERE type LIKE '%Classes%';

UPDATE public.list
SET type = replace(type, 'class', 'classis')
WHERE type LIKE '%class';

UPDATE public.list
SET type = replace(type, 'Class', 'Classis')
WHERE type LIKE '%Class';

UPDATE public.list
SET type = 'Infraclassis'
WHERE type = 'Infraclasse';


-- CHECK RESULT:

SELECT type, count(1)
FROM public.list
WHERE type NOT IN (SELECT ranks.type
                   FROM public.ranks)
  -- AND type ILIKE '%class%'
GROUP BY type
ORDER BY count(1) DESC;