-- Spaces:

UPDATE public.list
SET type = trim(type)
WHERE type LIKE ' %'
  OR type LIKE '% ';

UPDATE public.list
SET type = "left"(type, -1)
WHERE type LIKE '% ';

-- Tabs:

UPDATE public.list
SET type = replace(type, chr(9), '')
WHERE type LIKE (chr(9) || '%');

-- Incertae sedis:

UPDATE public.list
SET type = replace(type, ' (unaccepted)', '')
WHERE type LIKE '% (unaccepted)';

UPDATE public.list
SET type = replace(type, ' unassigned', '')
WHERE type LIKE '% unassigned';

UPDATE public.list
SET type = replace(type, ' Unassigned', '')
WHERE type LIKE '% Unassigned';

UPDATE public.list
SET type = replace(type, ' Incertae sedis', '')
WHERE type LIKE '% Incertae sedis';

UPDATE public.list
SET type = replace(type, ' incertae sedis', '')
WHERE type LIKE '% incertae sedis';

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

-- Divisio:

UPDATE public.list
SET type = replace(type, 'division', 'divisio')
WHERE type LIKE '%division%';

UPDATE public.list
SET type = replace(type, 'Division', 'Divisio')
WHERE type LIKE '%Division%';

-- Typos & languages - Genus:

UPDATE public.list
SET type = 'Genus'
WHERE type = 'Genera';

UPDATE public.list
SET type = 'Subgenus'
WHERE type = 'Subgenera';

-- Typos & languages - Varietas:

UPDATE public.list
SET type = 'Varietas'
WHERE type = 'Varietate';

UPDATE public.list
SET type = 'Varietas'
WHERE type = 'Varieties';

UPDATE public.list
SET type = 'Varietas'
WHERE type = 'Varietates';

UPDATE public.list
SET type = 'Varietas'
WHERE type = 'Variety';

-- species -> Species:

UPDATE public.list
SET type = 'Species'
WHERE type = 'species';

-- Typos & languages - Familia:

UPDATE public.list
SET type = 'Familia'
WHERE type = 'Familia Incertae sedis';

UPDATE public.list
SET type = 'Familia'
WHERE type = 'Familiae';

UPDATE public.list
SET type = 'Familia'
WHERE type = 'Family';

UPDATE public.list
SET type = 'Subfamilia'
WHERE type = 'Subfamily';

UPDATE public.list
SET type = 'Subfamilia'
WHERE type = 'Subfamilie';

UPDATE public.list
SET type = 'Subfamilia'
WHERE type = 'Subfamiliae';

-- Typos & languages - Subspecies:

UPDATE public.list
SET type = 'Subspecies'
WHERE type = 'Sub-Species';

UPDATE public.list
SET type = 'Subspecies'
WHERE type = 'Subpecies';

UPDATE public.list
SET type = 'Subspecies'
WHERE type = 'Susbspecies';

UPDATE public.list
SET type = 'Subspecies'
WHERE type = 'Subespecies';

UPDATE public.list
SET type = 'Subspecies'
WHERE type = 'Subspeccies';

UPDATE public.list
SET type = 'Subspecies'
WHERE type = 'Subspeies';

UPDATE public.list
SET type = 'Subspecies'
WHERE type = 'subspecies';

-- CHECK RESULT:

SELECT type, count(1)
FROM public.list
WHERE type NOT IN (SELECT ranks.type
                   FROM public.ranks)
  -- AND type ILIKE '%Notho%'
GROUP BY type
ORDER BY count(1) DESC;