CREATE OR REPLACE FUNCTION public.build_get_tree_cache(_language_key text, _page_url_from text, _page_url_to text)
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
               target.page_url
        FROM public.list target
        WHERE (target.page_url >= _page_url_from OR _page_url_from IS NULL)
        AND (target.page_url <= _page_url_to OR _page_url_to IS NULL)
        ORDER BY target.page_url
    LOOP

      RAISE NOTICE 'build_get_tree_cache(): processing id = %, page_url = %', _row.id, _row.page_url;

        INSERT INTO public.get_tree_cache AS t (id, result_on_languages)
        SELECT _row.id, jsonb_build_object(_language_key, (public.get_tree_by_id(_id := _row.id, _language_key := _language_key))::jsonb)
        ON CONFLICT (id) DO UPDATE
        SET result_on_languages = coalesce(t.result_on_languages, '{}'::jsonb) || excluded.result_on_languages;

      _counter = _counter + 1;
      RAISE NOTICE 'build_get_tree_cache(): % of % processed', _counter, _total;

    END LOOP;

END
$$ LANGUAGE 'plpgsql';


SELECT public.build_get_tree_cache('ru', 'Aaa', 'Baa');
SELECT public.build_get_tree_cache('ru', 'Baa', 'Caa');
SELECT public.build_get_tree_cache('ru', 'Caa', 'Daa');
SELECT public.build_get_tree_cache('ru', 'Daa', 'Eaa');
SELECT public.build_get_tree_cache('ru', 'Eaa', 'Faa');
SELECT public.build_get_tree_cache('ru', 'Faa', 'Gaa');
SELECT public.build_get_tree_cache('ru', 'Gaa', 'Haa');
SELECT public.build_get_tree_cache('ru', 'Haa', 'Iaa');
SELECT public.build_get_tree_cache('ru', 'Iaa', 'Jaa');
SELECT public.build_get_tree_cache('ru', 'Jaa', 'Kaa');
SELECT public.build_get_tree_cache('ru', 'Kaa', 'Laa');
SELECT public.build_get_tree_cache('ru', 'Laa', 'Maa');
SELECT public.build_get_tree_cache('ru', 'Maa', 'Naa');
SELECT public.build_get_tree_cache('ru', 'Naa', 'Oaa');
SELECT public.build_get_tree_cache('ru', 'Oaa', 'Paa');
SELECT public.build_get_tree_cache('ru', 'Paa', 'Qaa');
SELECT public.build_get_tree_cache('ru', 'Qaa', 'Raa');
SELECT public.build_get_tree_cache('ru', 'Raa', 'Saa');
SELECT public.build_get_tree_cache('ru', 'Saa', 'Taa');
SELECT public.build_get_tree_cache('ru', 'Taa', 'Vaa');
SELECT public.build_get_tree_cache('ru', 'Vaa', 'Xaa');
SELECT public.build_get_tree_cache('ru', 'Xaa', 'Yaa');
SELECT public.build_get_tree_cache('ru', 'Yaa', 'Zaa');
SELECT public.build_get_tree_cache('ru', 'Zaa', 'Zzz');


DROP FUNCTION IF EXISTS public.build_get_tree_cache(_language_key text, _page_url_from text, _page_url_to text);