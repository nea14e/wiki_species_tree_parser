CREATE OR REPLACE FUNCTION public.apply_parents(_page_url_from text, _page_url_to text)
  RETURNS void
  VOLATILE
AS
$$
DECLARE
  _row     record;
  _counter bigint;
  _total   bigint;
BEGIN
  SELECT count(1) INTO _total
  FROM public.list
  WHERE (page_url >= _page_url_from OR _page_url_from IS NULL)
    AND (page_url <= _page_url_to OR _page_url_to IS NULL);

  _counter = 0;

  FOR _row IN
    SELECT target.id,
           coalesce(target.parent_page_url_actual, target.parent_page_url) AS parent_page_url,
           parent.id AS parent_id
    FROM public.list target
      LEFT JOIN public.list parent ON parent.page_url = coalesce(target.parent_page_url_actual, target.parent_page_url)
    WHERE (target.page_url >= _page_url_from OR _page_url_from IS NULL)
    AND (target.page_url <= _page_url_to OR _page_url_to IS NULL)
    LOOP

      UPDATE public.list target
      SET parent_id = _row.parent_id
      WHERE target.id = _row.id;

      _counter = _counter + 1;
      IF _counter % 1000 = 0 THEN
        RAISE NOTICE 'apply_parents(): % of % processed', _counter, _total;
      END IF;

    END LOOP;

END
$$ LANGUAGE 'plpgsql';


SELECT public.apply_parents('Aaa', 'Baa');
SELECT public.apply_parents('Baa', 'Caa');
SELECT public.apply_parents('Caa', 'Daa');
SELECT public.apply_parents('Daa', 'Eaa');
SELECT public.apply_parents('Eaa', 'Faa');
SELECT public.apply_parents('Faa', 'Gaa');
SELECT public.apply_parents('Gaa', 'Haa');
SELECT public.apply_parents('Haa', 'Iaa');
SELECT public.apply_parents('Iaa', 'Jaa');
SELECT public.apply_parents('Jaa', 'Kaa');
SELECT public.apply_parents('Kaa', 'Laa');
SELECT public.apply_parents('Laa', 'Maa');
SELECT public.apply_parents('Maa', 'Naa');
SELECT public.apply_parents('Naa', 'Oaa');
SELECT public.apply_parents('Oaa', 'Paa');
SELECT public.apply_parents('Paa', 'Qaa');
SELECT public.apply_parents('Qaa', 'Raa');
SELECT public.apply_parents('Raa', 'Saa');
SELECT public.apply_parents('Saa', 'Taa');
SELECT public.apply_parents('Taa', 'Vaa');
SELECT public.apply_parents('Vaa', 'Xaa');
SELECT public.apply_parents('Xaa', 'Yaa');
SELECT public.apply_parents('Yaa', 'Zaa');
SELECT public.apply_parents('Zaa', 'Zzz');


SELECT count(1 WHERE parent_id IS NULL)       AS parent_id_is_null,
       count(1 WHERE parent_page_url IS NULL) AS parent_page_url_is_null,
       count(1)                               AS total_count
FROM public.list;


DROP FUNCTION IF EXISTS public.apply_parents(_page_url_from text, _page_url_to text);