CREATE OR REPLACE FUNCTION public.get_childes_by_id(_id bigint DEFAULT NULL::bigint,
                                           _language_key text DEFAULT NULL::text) RETURNS json
  STABLE
  LANGUAGE plpgsql
AS
$$
DECLARE
  _levels_json             jsonb = '[]'::jsonb; -- jsonb is stored in pre-parsed way so operations with him are more faster
  _level_object_json       jsonb = '{}'::jsonb;
  _level_items_json        jsonb = '[]'::jsonb;
  _cur_parent_title        text;
  _level_max_order         int;
  _level_min_order         int;
  _cur_rank                record;
BEGIN
  -- Show only childes of selected element. Childes may be on multiple levels.

  _level_min_order = -999;

  -- For cycle borders
  SELECT COALESCE(list.titles_by_languages ->> _language_key, list.title),
         "order"
         INTO _cur_parent_title, _level_max_order
  FROM public.list
         LEFT JOIN public.ranks ON ranks.type = list.type
  WHERE id = _id;

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

      SELECT jsonb_agg(t ORDER BY title_for_language)
             INTO _level_items_json
      FROM (
             SELECT id,
                    COALESCE(titles_by_languages ->> _language_key, title) AS title_for_language,    -- Latin name if not present
                    page_url,
                    image_url,
                    COALESCE(wikipedias_by_languages ->> _language_key,
                             wikipedias_by_languages ->> 'en')             AS wiki_url_for_language, -- English type if not present
                    _id   AS parent_id,
                    leaves_count,
                    FALSE AS is_expanded,  -- childes of current selected element does not expanded when them just loaded
                    FALSE AS is_selected  -- childes of current selected element does not selected when them just loaded
             FROM public.list
             WHERE parent_id = _id -- which parent is current element
               AND "type" = _cur_rank."type" -- only childes on current level. One parent may have childes on multiple levels and we want to put them separately
           ) t;

      -- RAISE NOTICE '_level_json: array: ''%''.', _level_json;
      -- RAISE NOTICE 'jsonb_array_length(_level_json): ''%''.', jsonb_array_length(_level_json);

      IF _level_items_json IS NOT NULL THEN -- if requested item does not have any childes then _level will be NULL which would lead to NULL entire _answer otherwise

        _level_object_json = jsonb_build_object(
            'type', _cur_rank."type",
            'title_on_language', _cur_rank.title_for_language,
            'items', _level_items_json,
            'level_parent_id', _id,
            'level_parent_title', _cur_parent_title,
            'is_level_has_selected_item', FALSE
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

  RETURN _levels_json::json;
END;
$$;