DROP FUNCTION IF EXISTS public.get_tree_by_id(_id bigint,
                                              _language_key text);

DROP FUNCTION IF EXISTS public.get_tree_by_id(
    _id bigint,
    _language_key1 text,
    _language_key2 text
);

CREATE OR REPLACE FUNCTION public.get_tree_by_id(
    _id bigint,
    _parent_mode parent_mode,
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
    _levels_json             jsonb    = '[]'::jsonb; -- jsonb is stored in pre-parsed way so operations with it are more faster
    _level_object_json       jsonb    = '{}'::jsonb;
    _level_items_json        jsonb    = '[]'::jsonb;
    _has_level_selected_item boolean;
    _next_parent_id          bigint;
    _cur_parent_id           bigint;
    _prev_parent_id          bigint;
    _prev_parents_ids        bigint[] = ARRAY []::bigint[];
    _cur_parent_title        text;
    _level_max_order         int;
    _level_min_order         int;
    _cur_rank                record;
    _cur_rank_type           text;
    _cur_rank_language1      text;
    _cur_rank_latin          text;
    _cur_parent_type         text;
    _prev_parent_type        text;
BEGIN

    /*_key_for_tree_cache = public.get_key_for_tree_cache(_language_key1, _language_key2);
    
    IF _language_key1 = 'ru' AND _language_key2 = 'latin' THEN
      SELECT result_on_languages -> _key_for_tree_cache
      INTO _cached_result
      FROM public.get_tree_cache
      WHERE id = _id;
    
      IF _cached_result IS NOT NULL THEN
        RETURN _cached_result::json;
      END IF;
    END IF;*/

    -- Для выбранного элемента (id = _id) подгружаем дочерние элементы всех уровней
    -- (дочерние могут располагаться на нескольких разных уровнях, поэтому цикл по уровням)
    -- Для границ цикла по уровням:
    SELECT CASE _parent_mode
               WHEN 'regular' THEN regular_ranks_only_parent_id
               WHEN 'named_only' THEN named_ranks_only_parent_id
               WHEN 'all' THEN parent_id
               END,
           ranks."type",
           ranks."order",
           CASE
               WHEN _language_key1 != 'latin'
                   THEN COALESCE(list.titles_by_languages ->> _language_key1, list.latin)
               ELSE list.latin
               END
    INTO _next_parent_id, _cur_parent_type, _level_max_order, _cur_parent_title
    FROM public.list
             LEFT JOIN public.ranks ON ranks.type = list.type
    WHERE id = _id;

    _level_min_order = -31999;

    RAISE NOTICE 'MAIN PARENT: _id = ''%'', _cur_parent_type = ''%'', _cur_parent_title = ''%'', _level_min_order = ''%'', _level_max_order = ''%''.',
        _id, _cur_parent_type, _cur_parent_title, _level_min_order, _level_max_order;

    -- Цикл по уровням дочерних элементов:
    FOR _cur_rank IN
        SELECT "type",
               titles_by_languages ->> _language_key1 AS rank_for_language1,
               latin                                  AS rank_latin
        FROM public.ranks
        WHERE ("order" < _level_max_order OR _level_max_order IS NULL)
          AND "order" >= _level_min_order
        ORDER BY "order"
        LOOP

            RAISE NOTICE 'CHILD _cur_rank: ''%''.', _cur_rank."type";

            SELECT JSONB_AGG(t ORDER BY title_for_language1)
            INTO _level_items_json
            FROM (SELECT id,
                         CASE
                             WHEN _language_key1 != 'latin' THEN titles_by_languages ->> _language_key1
                             ELSE latin
                             END AS title_for_language1,
                         CASE
                             WHEN _language_key2 = 'latin' THEN latin
                             WHEN _language_key2 IS NOT NULL THEN titles_by_languages ->> _language_key2
                             WHEN _language_key2 IS NULL THEN NULL
                             END AS title_for_language2,
                         latin   AS title_latin,
                         page_id,
                         image_url,
                         CASE _parent_mode
                             WHEN 'regular' THEN regular_ranks_only_parent_id
                             WHEN 'named_only' THEN named_ranks_only_parent_id
                             WHEN 'all' THEN parent_id
                             END AS parent_id,
                         leaves_count,
                         FALSE   AS is_expanded,
                         FALSE   AS is_selected
                  FROM public.list
                  WHERE (CASE _parent_mode
                             WHEN 'regular' THEN regular_ranks_only_parent_id
                             WHEN 'named_only' THEN named_ranks_only_parent_id
                             WHEN 'all' THEN parent_id
                      END) = _id                  -- дочерние элементы
                    AND "type" = _cur_rank."type" -- только текущего уровня
                    AND is_deleted = FALSE) t;

            IF _level_items_json IS NOT NULL THEN -- Если текущий уровень не имеет элементов, то будет NULL, что может испортить весь результат 
                _level_object_json = JSONB_BUILD_OBJECT(
                        'type', _cur_rank."type",
                        'rank_for_language1', _cur_rank.rank_for_language1,
                        'rank_latin', _cur_rank.rank_latin,
                        'items', _level_items_json,
                        'level_parent_id', _id,
                        'level_parent_title', _cur_parent_title,
                        'is_level_has_selected_item', FALSE
                                     );

                RAISE NOTICE 'CHILD _level_object_json: %', _level_object_json;

                _levels_json = JSONB_INSERT(
                        jsonb_in := _levels_json,
                        path := '{0}', -- put to the beginning of levels' list
                        replacement := _level_object_json,
                        insert_after := FALSE
                               );
            END IF;

        END LOOP; -- Цикл по уровням

    _cur_parent_id = _id;
    _prev_parents_ids = array_append(_prev_parents_ids, _id);

    -- Теперь поднимаемся вверх от выбранного элемента (_id) до корня дерева
    -- Цикл, пока родители не кончатся:
    WHILE TRUE
        LOOP

            _prev_parent_id = _cur_parent_id;
            _cur_parent_id = _next_parent_id;

            _prev_parent_type = _cur_parent_type;

            -- Если дошли до корня дерева или обнаружилось зацикливание (бывают битые данные)
            IF _cur_parent_id IS NULL OR _cur_parent_id = ANY(_prev_parents_ids) THEN
                RETURN JSONB_BUILD_OBJECT(
                    '_id', _id,
                    '_language_key1', _language_key1,
                    '_language_key2', _language_key2,
                    'levels', _levels_json
                )::json;
            END IF;

            -- Текущий родитель
            SELECT CASE _parent_mode
                       WHEN 'regular' THEN regular_ranks_only_parent_id
                       WHEN 'named_only' THEN named_ranks_only_parent_id
                       WHEN 'all' THEN parent_id
                   END,
                   ranks."type", -- иногда бывают битые виды рангов, в этом случае тут будет NULL
                   CASE
                       WHEN _language_key1 != 'latin'
                           THEN COALESCE(list.titles_by_languages ->> _language_key1, list.latin)
                       ELSE list.latin
                   END
            INTO _next_parent_id, _cur_parent_type, _cur_parent_title
            FROM public.list
                     LEFT JOIN public.ranks ON ranks.type = list.type
            WHERE id = _cur_parent_id;

            RAISE NOTICE 'CURRENT PARENT: _cur_parent_id = ''%'', _cur_parent_type = ''%'', _cur_parent_title = ''%''.', 
                _cur_parent_id, _cur_parent_type, _cur_parent_title;

            SELECT JSONB_AGG(t ORDER BY title_for_language1),
                   (SUM(CASE WHEN t.is_selected THEN 1 ELSE 0 END) > 0)::boolean
            INTO _level_items_json, _has_level_selected_item
            FROM (SELECT id,
                         CASE
                             WHEN _language_key1 != 'latin' THEN titles_by_languages ->> _language_key1
                             ELSE latin
                             END         AS title_for_language1,
                         CASE
                             WHEN _language_key2 = 'latin' THEN latin
                             WHEN _language_key2 IS NOT NULL THEN titles_by_languages ->> _language_key2
                             WHEN _language_key2 IS NULL THEN NULL
                             END         AS title_for_language2,
                         latin           AS title_latin,
                         page_id,
                         image_url,
                         CASE _parent_mode
                             WHEN 'regular' THEN regular_ranks_only_parent_id
                             WHEN 'named_only' THEN named_ranks_only_parent_id
                             WHEN 'all' THEN parent_id
                             END         AS parent_id,
                         leaves_count,
                         COALESCE((id = _prev_parent_id)::boolean OR (id = _id)::boolean,
                                  FALSE) AS is_expanded,
                         COALESCE((id = _id)::boolean,
                                  FALSE) AS is_selected
                  FROM public.list
                  WHERE (CASE _parent_mode
                             WHEN 'regular' THEN regular_ranks_only_parent_id
                             WHEN 'named_only' THEN named_ranks_only_parent_id
                             WHEN 'all' THEN parent_id
                      END) = _cur_parent_id        -- Элементы, дочерние к текущему родителю
                    AND "type" = _prev_parent_type -- Текущий родитель может иметь дочерние на нескольких уровнях. Тогда подгружаем только уровень с прошлым родителем
                    AND is_deleted = FALSE) t;

            IF _level_items_json IS NOT NULL THEN -- Если текущий уровень не имеет элементов, то будет NULL, что может испортить весь результат
                
                SELECT r."type" AS "type",
                       r.titles_by_languages ->> _language_key1 AS rank_for_language1,
                       r."type"                                 AS rank_latin
                INTO _cur_rank_type, _cur_rank_language1, _cur_rank_latin
                FROM public.list l
                    LEFT JOIN public.ranks r ON l.type = r.type
                WHERE l.id = _prev_parent_id;  -- Предыдущий родитель находится на текущем уровне

                _level_object_json = JSONB_BUILD_OBJECT(
                        'type', _cur_rank_type,
                        'rank_for_language1', _cur_rank_language1,
                        'rank_latin', _cur_rank_latin,
                        'items', _level_items_json,
                        'level_parent_id', _cur_parent_id,
                        'level_parent_title', _cur_parent_title,
                        'is_level_has_selected_item', _has_level_selected_item
                );

                RAISE NOTICE 'CURRENT PARENT _level_object_json: %', _level_object_json;

                _levels_json = JSONB_INSERT(
                        jsonb_in := _levels_json,
                        path := '{0}', -- put to the beginning of levels' list
                        replacement := _level_object_json,
                        insert_after := FALSE
                               );

            END IF;

        END LOOP; -- Цикл по родителям
END;
$$;

/*
SELECT public.get_tree_by_id(
  _id := 69437,
  _parent_mode := 'regular',
  _language_key1 := 'ru',
  _language_key2 := 'latin'
);

SELECT public.get_tree_by_id(
  _id := 68768,
  _parent_mode := 'regular',
  _language_key1 := 'latin',
  _language_key2 := 'ru'
);

SELECT public.get_tree_by_id(
  _id := 68768,
  _parent_mode := 'regular',
  _language_key1 := 'ru',
  _language_key2 := NULL
);

SELECT public.get_tree_by_id(
  _id := 68768,
  _parent_mode := 'regular',
  _language_key1 := 'en',
  _language_key2 := 'ru'
);
*/