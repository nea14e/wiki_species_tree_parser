CREATE OR REPLACE FUNCTION public.get_tree_default(_language_key text DEFAULT NULL::text) RETURNS json
  STABLE
  LANGUAGE plpgsql
AS
$$
DECLARE
  _translation_object_json jsonb = '{}'::jsonb; -- jsonb is stored in pre-parsed way so operations with him are more faster
  _levels_json             jsonb = '[]'::jsonb;
  _level_object_json       jsonb = '{}'::jsonb;
  _level_items_json        jsonb = '[]'::jsonb;
  _cur_rank                record;
BEGIN
  -- When page is opened with default routing, show first 3 levels fully

  -- Cycle by _cur_level_type:
  FOR _cur_rank IN
    SELECT "type"                                                  AS "type",
           COALESCE(titles_by_languages ->> _language_key, "type") AS title_for_language -- Latin type if not present
    FROM public.ranks
    ORDER BY "order" DESC -- we are going from top level to bottom
    LIMIT 3 -- show 3 highest levels
    LOOP

      -- RAISE NOTICE 'NEXT _cur_level_type: ''%''.', _cur_level_type;

      SELECT jsonb_agg(t ORDER BY title_for_language) INTO _level_items_json
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
                    FALSE                                                  AS is_expanded,
                    FALSE                                                  AS is_selected
             FROM public.list
             WHERE "type" = _cur_rank."type"
           ) t;

      -- RAISE NOTICE '_level_json: array: ''%''.', _level_json;
      -- RAISE NOTICE 'jsonb_array_length(_level_json): ''%''.', jsonb_array_length(_level_json);

      _level_object_json = jsonb_build_object(
          'type', _cur_rank."type",
          'title_on_language', _cur_rank.title_for_language,
          'items', _level_items_json,
          'level_parent_id', NULL,
          'level_parent_title', NULL,
          'is_level_has_selected_item', FALSE
        );
      -- RAISE NOTICE '_level_json: object: ''%''.', _level_json;

      _levels_json = jsonb_insert(
          jsonb_in := _levels_json,
          path := '{-1}', -- put to the end of levels' list
          replacement := _level_object_json,
          insert_after := TRUE
        );

    END LOOP; -- Cycle by _cur_level_type:


  RETURN jsonb_build_object(
      '_id', NULL,
      '_language_key', _language_key,
      'levels', _levels_json
    )::json;
END;
$$;