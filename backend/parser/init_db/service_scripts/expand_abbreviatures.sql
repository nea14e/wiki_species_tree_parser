UPDATE public.list
SET title = regexp_replace(title, '<abbr title="(.+?)">.+?</abbr>\.', '\1', 'g')
WHERE title LIKE '%<abbr title=%';