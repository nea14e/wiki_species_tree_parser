ALTER TABLE public.list
  ADD COLUMN IF NOT EXISTS parent_page_url_actual text;

CREATE OR REPLACE FUNCTION public.correct_list_with_synonyms__parent_page_url(_page_url_from text, _page_url_to text)
  RETURNS void AS
$$
BEGIN
  DROP TABLE IF EXISTS _synonyms;

  CREATE TEMP TABLE _synonyms (
    "value" text PRIMARY KEY,
    result_page_url text NOT NULL
  ) ON COMMIT DROP;

  INSERT INTO _synonyms("value", result_page_url)
  SELECT "value", result_page_url
  FROM (
         SELECT unnest(page_url_synonyms) "value",
                result_page_url
         FROM public.synonyms
       ) t
  WHERE "value" != result_page_url;

  UPDATE public.list ll
  SET parent_page_url_actual = syn.result_page_url
  FROM _synonyms syn
  WHERE ll.parent_page_url = syn.value
    AND (ll.parent_page_url >= _page_url_from OR _page_url_from IS NULL)
    AND (ll.parent_page_url < _page_url_to OR _page_url_to IS NULL);
END;
$$ LANGUAGE 'plpgsql';

SELECT public.correct_list_with_synonyms__parent_page_url('Aaa', 'Baa');
SELECT public.correct_list_with_synonyms__parent_page_url('Baa', 'Caa');
SELECT public.correct_list_with_synonyms__parent_page_url('Caa', 'Daa');
SELECT public.correct_list_with_synonyms__parent_page_url('Daa', 'Eaa');
SELECT public.correct_list_with_synonyms__parent_page_url('Eaa', 'Faa');
SELECT public.correct_list_with_synonyms__parent_page_url('Faa', 'Gaa');
SELECT public.correct_list_with_synonyms__parent_page_url('Gaa', 'Haa');
SELECT public.correct_list_with_synonyms__parent_page_url('Haa', 'Iaa');
SELECT public.correct_list_with_synonyms__parent_page_url('Iaa', 'Jaa');
SELECT public.correct_list_with_synonyms__parent_page_url('Jaa', 'Kaa');
SELECT public.correct_list_with_synonyms__parent_page_url('Kaa', 'Laa');
SELECT public.correct_list_with_synonyms__parent_page_url('Laa', 'Maa');
SELECT public.correct_list_with_synonyms__parent_page_url('Maa', 'Naa');
SELECT public.correct_list_with_synonyms__parent_page_url('Naa', 'Oaa');
SELECT public.correct_list_with_synonyms__parent_page_url('Oaa', 'Paa');
SELECT public.correct_list_with_synonyms__parent_page_url('Paa', 'Qaa');
SELECT public.correct_list_with_synonyms__parent_page_url('Qaa', 'Raa');
SELECT public.correct_list_with_synonyms__parent_page_url('Raa', 'Saa');
SELECT public.correct_list_with_synonyms__parent_page_url('Saa', 'Taa');
SELECT public.correct_list_with_synonyms__parent_page_url('Taa', 'Vaa');
SELECT public.correct_list_with_synonyms__parent_page_url('Vaa', 'Xaa');
SELECT public.correct_list_with_synonyms__parent_page_url('Xaa', 'Yaa');
SELECT public.correct_list_with_synonyms__parent_page_url('Yaa', 'Zaa');
SELECT public.correct_list_with_synonyms__parent_page_url('Zaa', 'Zzz');



SELECT count(1) AS replaced_synonyms_count
FROM public.list
WHERE list.parent_page_url_actual IS NOT NULL;

SELECT sum(array_length(page_url_synonyms, 1)) AS synonyms_count
FROM public.synonyms;

SELECT count(1) AS total_records_count
FROM public.list;



DROP FUNCTION IF EXISTS public.correct_list_with_synonyms__parent_page_url(text, text);