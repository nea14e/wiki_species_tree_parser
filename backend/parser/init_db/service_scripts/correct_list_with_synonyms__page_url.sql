ALTER TABLE public.list
  ADD COLUMN IF NOT EXISTS is_deleted bool NOT NULL DEFAULT FALSE;

CREATE OR REPLACE FUNCTION public.correct_list_with_synonyms__page_url(_page_url_from text, _page_url_to text)
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
  SET is_deleted = TRUE
  FROM _synonyms syn
  WHERE ll.page_url = syn.value
    AND (ll.page_url >= _page_url_from OR _page_url_from IS NULL)
    AND (ll.page_url < _page_url_to OR _page_url_to IS NULL);
END;
$$ LANGUAGE 'plpgsql';


SELECT public.correct_list_with_synonyms__page_url('Aaa', 'Baa');
SELECT public.correct_list_with_synonyms__page_url('Baa', 'Caa');
SELECT public.correct_list_with_synonyms__page_url('Caa', 'Daa');
SELECT public.correct_list_with_synonyms__page_url('Daa', 'Eaa');
SELECT public.correct_list_with_synonyms__page_url('Eaa', 'Faa');
SELECT public.correct_list_with_synonyms__page_url('Faa', 'Gaa');
SELECT public.correct_list_with_synonyms__page_url('Gaa', 'Haa');
SELECT public.correct_list_with_synonyms__page_url('Haa', 'Iaa');
SELECT public.correct_list_with_synonyms__page_url('Iaa', 'Jaa');
SELECT public.correct_list_with_synonyms__page_url('Jaa', 'Kaa');
SELECT public.correct_list_with_synonyms__page_url('Kaa', 'Laa');
SELECT public.correct_list_with_synonyms__page_url('Laa', 'Maa');
SELECT public.correct_list_with_synonyms__page_url('Maa', 'Naa');
SELECT public.correct_list_with_synonyms__page_url('Naa', 'Oaa');
SELECT public.correct_list_with_synonyms__page_url('Oaa', 'Paa');
SELECT public.correct_list_with_synonyms__page_url('Paa', 'Qaa');
SELECT public.correct_list_with_synonyms__page_url('Qaa', 'Raa');
SELECT public.correct_list_with_synonyms__page_url('Raa', 'Saa');
SELECT public.correct_list_with_synonyms__page_url('Saa', 'Taa');
SELECT public.correct_list_with_synonyms__page_url('Taa', 'Vaa');
SELECT public.correct_list_with_synonyms__page_url('Vaa', 'Xaa');
SELECT public.correct_list_with_synonyms__page_url('Xaa', 'Yaa');
SELECT public.correct_list_with_synonyms__page_url('Yaa', 'Zaa');
SELECT public.correct_list_with_synonyms__page_url('Zaa', 'Zzz');



SELECT count(1) AS deleted_synonyms_count
FROM public.list
WHERE is_deleted = TRUE;

SELECT sum(array_length(page_url_synonyms, 1)) AS synonyms_count
FROM public.synonyms;

SELECT count(1) AS total_records_count
FROM public.list;



DROP FUNCTION IF EXISTS public.correct_list_with_synonyms__page_url(text, text);