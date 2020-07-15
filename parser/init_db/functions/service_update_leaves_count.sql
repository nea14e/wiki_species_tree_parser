CREATE OR REPLACE FUNCTION public.service_update_leaves_count() RETURNS text
  STABLE
  LANGUAGE plpgsql
AS
$$
DECLARE
  _leaves_by_themselves bigint;
  _rows_updated         bigint;
BEGIN
  -- Remove all previous counts:
  -- noinspection SqlWithoutWhere
  UPDATE public.list
  SET leaves_count = NULL;

  -- Mark leaves (items with no childes)
  UPDATE public.list
  SET leaves_count = 1
  WHERE NOT EXISTS(SELECT 1
                   FROM public.list child
                   WHERE child.parent_id = list.id);

  -- Update counts in parents
  WHILE TRUE
    LOOP

      UPDATE public.list target
      SET leaves_count = source.sum_from_childs
      FROM (SELECT child.parent_id,
                   SUM(child.leaves_count)                                     AS sum_from_childs,
                   SUM(CASE WHEN child.leaves_count IS NULL THEN 1 ELSE 0 END) AS unfilled_childs_count
            FROM public.list child
            GROUP BY child.parent_id) AS source
      WHERE target.id = source.parent_id
        AND target.leaves_count IS NULL -- only not filled yet
        AND source.unfilled_childs_count = 0; -- only if all childes are filled already

      GET DIAGNOSTICS _rows_updated = ROW_COUNT;
      IF _rows_updated = 0 THEN
        EXIT; -- break infinite while
      END IF;
    END LOOP;

  -- Un-Mark leaves (items with no childes)
  UPDATE public.list
  SET leaves_count = 0
  WHERE NOT EXISTS(SELECT 1
                   FROM public.list child
                   WHERE child.parent_id = list.id);

  GET DIAGNOSTICS _leaves_by_themselves = ROW_COUNT;

  RETURN 'Updating of leaves completed. Found ' || _leaves_by_themselves::text || ' leaves by themselves.';
END;
$$;

ALTER FUNCTION service_update_leaves_count() OWNER TO postgres;

