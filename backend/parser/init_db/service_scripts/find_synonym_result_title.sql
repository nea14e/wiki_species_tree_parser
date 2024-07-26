CREATE OR REPLACE FUNCTION public.find_synonym_result_title(_title_from text, _title_to text)
  RETURNS void
  VOLATILE
AS
$$
UPDATE public.synonyms
SET result_page_url = replace(title, ' ', '_')
WHERE replace(title, ' ', '_') = ANY (page_url_synonyms)
  AND (title >= _title_from OR _title_from IS NULL)
  AND (title < _title_to OR _title_to IS NULL);
$$
  LANGUAGE SQL;



SELECT public.find_synonym_result_title(NULL, 'Gaa');
SELECT public.find_synonym_result_title('Gaa', 'Kaa');
SELECT public.find_synonym_result_title('Kaa', 'Raa');
SELECT public.find_synonym_result_title('Raa', NULL);



SELECT count(1) AS errors_count
FROM public.synonyms
WHERE result_page_url IS NULL;

SELECT count(1) AS total_count
FROM public.synonyms;



DROP FUNCTION if EXISTS public.find_synonym_result_title(text, text);