CREATE OR REPLACE FUNCTION public.get_tree(_id bigint = NULL)
  RETURNS json AS
$$
DECLARE
  _answer         jsonb = '[]'::jsonb; -- jsonb is stored in pre-parsed way so operations with him are more faster
  _level          jsonb = '[]'::jsonb;
  _level_ids      bigint[];
  _parent_id      bigint;
  _prev_parent_id bigint;
BEGIN
  IF _id IS NULL THEN
    -- When page is opened with default routing, show first 3 levels fully

    -- Level 1 (full)

    SELECT jsonb_agg(t),
           array_agg(t.id)
           INTO _level, _level_ids
    FROM (
           SELECT *, FALSE AS is_expanded, FALSE AS is_selected
           FROM public.list
           WHERE parent_id IS NULL -- without parents
         ) t;

    _answer = jsonb_insert(
        jsonb_in := _answer,
        path := '{-1}',
        replacement := _level,
        insert_after := TRUE
      );

    -- Level 2 (full)

    SELECT jsonb_agg(t),
           array_agg(t.id)
           INTO _level, _level_ids
    FROM (
           SELECT *, FALSE AS is_expanded, FALSE AS is_selected
           FROM public.list
           WHERE parent_id = ANY (_level_ids) -- which parents were selected on level 1
         ) t;

    _answer = jsonb_insert(
        jsonb_in := _answer,
        path := '{-1}',
        replacement := _level,
        insert_after := TRUE
      );

    -- Level 3 (full)

    SELECT jsonb_agg(t),
           array_agg(t.id)
           INTO _level, _level_ids
    FROM (
           SELECT *, FALSE AS is_expanded, FALSE AS is_selected
           FROM public.list
           WHERE parent_id = ANY (_level_ids) -- which parents were selected on level 2
         ) t;

    _answer = jsonb_insert(
        jsonb_in := _answer,
        path := '{-1}',
        replacement := _level,
        insert_after := TRUE
      );

  ELSE
    -- Show requested element, its childes and all previous levels

    _parent_id = _id;
    _prev_parent_id = NULL;
    WHILE TRUE
      LOOP

        SELECT jsonb_agg(t) INTO _level
        FROM (
               SELECT *,
                      COALESCE((id = _prev_parent_id)::boolean, FALSE) AS is_expanded,
                      COALESCE((id = _id)::boolean, FALSE)             AS is_selected
               FROM public.list
               WHERE parent_id IS NOT DISTINCT FROM _parent_id -- which parents are current parent (note: "=" does not work for level 1 since one has _parent_id = NULL)
             ) t;

        IF _level IS NOT NULL THEN -- if requested item does not have any childes then _level will be NULL which would lead to NULL entire _answer otherwise
          _answer = jsonb_insert(
              jsonb_in := _answer,
              path := '{0}',
              replacement := _level,
              insert_after := FALSE
            );
        END IF;

        IF _parent_id IS NULL THEN
          EXIT; -- break the WHILE LOOP - we handled level 1 just now
        END IF;

        _prev_parent_id = _parent_id;

        -- level up (select parent item of current level and set it's parent as new current parent to find all items on it's level)
        SELECT parent_id INTO _parent_id -- note: may be NULL for level 1, continue working anyway to handle this level
        FROM public.list
        WHERE id = _parent_id;

      END LOOP;

  END IF;

  RETURN _answer::json;
END;
$$ LANGUAGE 'plpgsql';