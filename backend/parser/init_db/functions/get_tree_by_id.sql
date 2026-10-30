DROP FUNCTION IF EXISTS public.get_tree_by_id(_id bigint,
                                              _language_key text);

CREATE OR REPLACE FUNCTION public.get_tree_by_id(
    _id bigint,
    _language_key1 text,
    _language_key2 text DEFAULT NULL::text
) RETURNS json
  STABLE
  LANGUAGE plpgsql
AS
$$
DECLARE
  _key_for_tree_cache      text;
  _cached_result           jsonb;
  _levels_json             jsonb = '[]'::jsonb; -- jsonb is stored in pre-parsed way so operations with it are more faster
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
  _last_rank_type          text;
  _last_rank_for_language1 text;
  _last_rank_latin text;
BEGIN
  -- Show requested element, its childes and all previous levels

  _key_for_tree_cache = public.get_key_for_tree_cache(_language_key1, _language_key2);
  
  IF _language_key1 = 'ru' AND _language_key2 = 'latin' THEN
      SELECT result_on_languages -> _key_for_tree_cache
      INTO _cached_result
      FROM public.get_tree_cache
      WHERE id = _id;
    
      IF _cached_result IS NOT NULL THEN
        RETURN _cached_result::json;
      END IF;
  END IF;

  -- Cycle by parents
  _cur_parent_id = _id;
  _prev_parent_id = NULL;
  _level_min_order = -31999;
  WHILE TRUE
    LOOP

      -- For cycle borders and future level up (select parent item of current level and set it's parent as next parent to find all items on it's level)
      SELECT parent_id,
             CASE WHEN _language_key1 != 'latin'
                THEN COALESCE(list.titles_by_languages ->> _language_key1, list.latin)
                ELSE list.latin
             END,
             "order"
             INTO _next_parent_id, _cur_parent_title, _level_max_order
      FROM public.list
             LEFT JOIN public.ranks ON ranks.type = list.type
      WHERE id = _cur_parent_id;

      RAISE NOTICE 'NEXT PARENT: _cur_parent_id = ''%'', _level_bottom_order = ''%'', _level_top_order = ''%''.', _cur_parent_id, _level_min_order, _level_max_order;

      -- One parent may have childes on multiple levels and we want to put them separately. So, we have to use inner cycle:
      -- Cycle by _cur_rank:
      FOR _cur_rank IN
          SELECT "type",
                 titles_by_languages ->> _language_key1 AS rank_for_language1,
                 "type" AS rank_latin
        FROM public.ranks
        WHERE ("order" < _level_max_order OR _level_max_order IS NULL) -- load items with all highest levels when current level's "_cur_parent_id IS NULL"
          AND "order" >= _level_min_order
        ORDER BY "order" ASC -- we are going from bottom level to top (each time we do up to next parent)
        LOOP

          RAISE NOTICE 'NEXT _cur_rank: ''%''.', _cur_rank;

          SELECT jsonb_agg(t ORDER BY title_for_language1),
                 SUM(CASE WHEN t.is_selected THEN 1 ELSE 0 END)
                 INTO _level_items_json, _has_level_selected_item
          FROM (
                 SELECT id,
                        CASE 
                            WHEN _language_key1 != 'latin' THEN titles_by_languages ->> _language_key1
                            ELSE latin
                        END AS title_for_language1,
                        CASE
                            WHEN _language_key2 = 'latin' THEN latin
                            WHEN _language_key2 IS NOT NULL THEN titles_by_languages ->> _language_key2
                            WHEN _language_key2 IS NULL THEN NULL
                        END AS title_for_language2,
                        latin AS title_latin,
                        page_id,
                        image_url,
                        parent_id,
                        leaves_count,
                        COALESCE((id = _prev_parent_id)::boolean OR (id = _id)::boolean,
                                 FALSE)                                        AS is_expanded,
                        COALESCE((id = _id)::boolean,
                                 FALSE)                                        AS is_selected
                 FROM public.list
                 WHERE parent_id = _cur_parent_id -- which parents are current parent (note: "=" does not work for level 1 since one has _parent_id = NULL)
                   AND "type" = _cur_rank."type" -- only childes on current level. One parent may have childes on multiple levels and we want to put them separately
                   AND is_deleted = FALSE
               ) t;

          RAISE NOTICE '_level_items_json: array: ''%''.', _level_items_json;
          RAISE NOTICE 'jsonb_array_length(_level_items_json): ''%''.', jsonb_array_length(_level_items_json);

          IF _level_items_json IS NOT NULL THEN -- if requested item does not have any childes then _level will be NULL which would lead to NULL entire _answer otherwise

            _level_object_json = jsonb_build_object(
                'type', _cur_rank."type",
                'rank_for_language1', _cur_rank.rank_for_language1,
                'rank_latin', _cur_rank.rank_latin,
                'items', _level_items_json,
                'level_parent_id', _cur_parent_id,
                'level_parent_title', _cur_parent_title,
                'is_level_has_selected_item', _has_level_selected_item
              );

            RAISE NOTICE '_level_object_json: object: ''%''.', _level_object_json;

            _levels_json = jsonb_insert(
                jsonb_in := _levels_json,
                path := '{0}', -- put to the beginning of levels' list
                replacement := _level_object_json,
                insert_after := FALSE
              );

          END IF;

        END LOOP;  -- cycle by _cur_rank

      IF _cur_parent_id = _next_parent_id THEN
        EXIT;  -- to avoid infinity loop when such items present
      END IF;

      -- Level up:
      -- move level parents
      _prev_parent_id = _cur_parent_id;
      _cur_parent_id = _next_parent_id;
      _next_parent_id = NULL;
      -- move level borders
      _level_min_order = _level_max_order;
      _level_max_order = NULL;

      -- top level
      IF _cur_parent_id IS NULL THEN

        SELECT ranks.type,
               ranks.titles_by_languages ->> _language_key1,
               ranks.type
               INTO _last_rank_type, _last_rank_for_language1, _last_rank_latin
        FROM public.list
               LEFT JOIN public.ranks ON ranks.type = list.type
        WHERE id = _prev_parent_id;

        RAISE NOTICE 'TOP LEVEL: _last_rank_type = ''%'', _last_rank_for_language1 = ''%''.', _last_rank_type, _last_rank_for_language1;

        SELECT jsonb_agg(t ORDER BY title_for_language1),
               SUM(CASE WHEN t.is_selected THEN 1 ELSE 0 END)
               INTO _level_items_json, _has_level_selected_item
        FROM (
               SELECT id,
                      CASE
                          WHEN _language_key1 != 'latin' THEN titles_by_languages ->> _language_key1
                          ELSE latin
                      END AS title_for_language1,
                      CASE
                          WHEN _language_key2 = 'latin' THEN latin
                          WHEN _language_key2 IS NOT NULL THEN titles_by_languages ->> _language_key2
                          WHEN _language_key2 IS NULL THEN NULL
                      END AS title_for_language2,
                      latin AS title_latin,
                      page_id,
                      image_url,
                      parent_id,
                      leaves_count,
                      COALESCE((id = _prev_parent_id)::boolean OR (id = _id)::boolean,
                               FALSE)                                        AS is_expanded,
                      COALESCE((id = _id)::boolean,
                               FALSE)                                        AS is_selected
               FROM public.list
               WHERE id = _prev_parent_id
             ) t;

        RAISE NOTICE 'TOP _level_items_json: array: ''%''.', _level_items_json;
        RAISE NOTICE 'TOP jsonb_array_length(_level_items_json): ''%''.', jsonb_array_length(_level_items_json);

        IF _level_items_json IS NOT NULL THEN -- if requested item does not have any childes then _level will be NULL which would lead to NULL entire _answer otherwise

          _level_object_json = jsonb_build_object(
              'type', _last_rank_type,
              'rank_for_language1', _last_rank_for_language1,
              'rank_latin', _last_rank_latin,
              'items', _level_items_json,
              'level_parent_id', NULL,
              'level_parent_title', NULL,
              'is_level_has_selected_item', _has_level_selected_item
            );

          RAISE NOTICE 'TOP _level_object_json: object: ''%''.', _level_object_json;

          _levels_json = jsonb_insert(
              jsonb_in := _levels_json,
              path := '{0}', -- put to the beginning of levels' list
              replacement := _level_object_json,
              insert_after := FALSE
            );

        END IF;

        EXIT;

      END IF;

    END LOOP; -- cycle by parents

  RETURN jsonb_build_object(
      '_id', _id,
      '_language_key1', _language_key1,
      '_language_key2', _language_key2,
      'levels', _levels_json
    )::json;
END;
$$;

/*
SELECT public.get_tree_by_id(
  _id := 222,
  _language_key1 := 'ru',
  _language_key2 := 'latin'
);

SELECT public.get_tree_by_id(
  _id := 222,
  _language_key1 := 'latin',
  _language_key2 := 'ru'
);

SELECT public.get_tree_by_id(
  _id := 222,
  _language_key1 := 'ru',
  _language_key2 := NULL
);

SELECT public.get_tree_by_id(
  _id := 222,
  _language_key1 := 'en',
  _language_key2 := 'ru'
);
*/