CREATE OR REPLACE FUNCTION public.get_tree_by_id(_id bigint DEFAULT NULL::bigint,
                                           _language_key text DEFAULT NULL::text) RETURNS json
  STABLE
  LANGUAGE plpgsql
AS
$$
DECLARE
  _translation_object_json jsonb = '{}'::jsonb; -- jsonb is stored in pre-parsed way so operations with him are more faster
  _levels_json             jsonb = '[]'::jsonb;
  _level_object_json       jsonb = '{}'::jsonb;
  _level_items_json        jsonb = '[]'::jsonb;
  _has_level_selected_item boolean;
  _next_parent_id          bigint;
  _cur_parent_id           bigint;
  _cur_parent_title        text;
  _prev_parent_id          bigint;
  _level_max_order         int;
  _level_min_order         int;
  _cur_rank                record;
BEGIN
  -- Show requested element, its childes and all previous levels

  -- Cycle by parents
  _cur_parent_id = _id;
  _prev_parent_id = NULL;
  _level_min_order = -999;
  WHILE TRUE
    LOOP

      -- For cycle borders and future level up (select parent item of current level and set it's parent as next parent to find all items on it's level)
      SELECT parent_id,
             COALESCE(list.titles_by_languages ->> _language_key, list.title),
             "order"
             INTO _next_parent_id, _cur_parent_title, _level_max_order
      FROM public.list
             LEFT JOIN public.ranks ON ranks.type = list.type
      WHERE id = _cur_parent_id;

      -- RAISE NOTICE 'NEXT PARENT: _cur_parent_id = ''%'', _level_bottom_order = ''%'', _level_top_order = ''%''.', _cur_parent_id, _level_min_order, _level_max_order;

      -- One parent may have childes on multiple levels and we want to put them separately. So, we have to use inner cycle:
      -- Cycle by _cur_level_type:
      FOR _cur_rank IN
        SELECT "type"                                                  AS "type",
               COALESCE(titles_by_languages ->> _language_key, "type") AS title_for_language -- Latin type if not present
        FROM public.ranks
        WHERE ("order" < _level_max_order OR _level_max_order IS NULL) -- load items with all highest levels when current level's "_cur_parent_id IS NULL"
          AND "order" >= _level_min_order
        ORDER BY "order" ASC -- we are going from bottom level to top (each time we do up to next parent)
        LOOP

          -- RAISE NOTICE 'NEXT _cur_level_type: ''%''.', _cur_level_type;

          SELECT jsonb_agg(t ORDER BY title_for_language),
                 SUM(CASE WHEN t.is_selected THEN 1 ELSE 0 END)
                 INTO _level_items_json, _has_level_selected_item
          FROM (
                 SELECT id,
                        title AS title_latin,
                        COALESCE(titles_by_languages ->> _language_key, title) AS title_for_language,    -- Latin name if not present
                        page_url,
                        image_url,
                        COALESCE(wikipedias_by_languages ->> _language_key,
                                 wikipedias_by_languages ->> 'en')             AS wiki_url_for_language, -- English wiki if not present
                        parent_id,
                        leaves_count,
                        COALESCE((id = _prev_parent_id)::boolean OR (id = _id)::boolean,
                                 FALSE)                                        AS is_expanded,
                        COALESCE((id = _id)::boolean,
                                 FALSE)                                        AS is_selected
                 FROM public.list
                 WHERE parent_id IS NOT DISTINCT FROM _cur_parent_id -- which parents are current parent (note: "=" does not work for level 1 since one has _parent_id = NULL)
                   AND "type" = _cur_rank."type" -- only childes on current level. One parent may have childes on multiple levels and we want to put them separately
               ) t;

          -- RAISE NOTICE '_level_json: array: ''%''.', _level_json;
          -- RAISE NOTICE 'jsonb_array_length(_level_json): ''%''.', jsonb_array_length(_level_json);

          IF _level_items_json IS NOT NULL THEN -- if requested item does not have any childes then _level will be NULL which would lead to NULL entire _answer otherwise

            _level_object_json = jsonb_build_object(
                'type', _cur_rank."type",
                'title_on_language', _cur_rank.title_for_language,
                'items', _level_items_json,
                'level_parent_id', _cur_parent_id,
                'level_parent_title', _cur_parent_title,
                'is_level_has_selected_item', _has_level_selected_item
              );

            -- RAISE NOTICE '_level_json: object: ''%''.', _level_json;

            _levels_json = jsonb_insert(
                jsonb_in := _levels_json,
                path := '{0}', -- put to the beginning of levels' list
                replacement := _level_object_json,
                insert_after := FALSE
              );

          END IF;

        END LOOP;
      -- cycle by _cur_level_type

      IF _cur_parent_id IS NULL THEN
        EXIT; -- break the WHILE LOOP - we handled the highest level just now
      END IF;

      -- Level up:
      -- move level parents
      _prev_parent_id = _cur_parent_id;
      _cur_parent_id = _next_parent_id;
      _next_parent_id = NULL;
      -- move level borders
      _level_min_order = _level_max_order;
      _level_max_order = NULL;

    END LOOP; -- cycle by parents

  RETURN jsonb_build_object(
      '_id', _id,
      '_language_key', _language_key,
      'levels', _levels_json
    )::json;
END;
$$;