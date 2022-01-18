CREATE OR REPLACE FUNCTION public.get_filling_stats(_groups_count int)
  RETURNS json
AS
$$
SELECT json_agg(tttt ORDER BY group_number)
FROM (
       SELECT group_number,
              title_from,
              title_to,
              total,
              stage_2,
              stage_2_percent,
              '#' ||
              lpad(to_hex(((100 - stage_2_percent) / 100.0 * 255)::int), 2, '0') ||
              lpad(to_hex((stage_2_percent / 100.0 * 255)::int), 2, '0') ||
              '00' AS stage_2_color,
              stage_3,
              stage_3_percent,
              '#' ||
              lpad(to_hex(((100 - stage_3_percent) / 100.0 * 255)::int), 2, '0') ||
              lpad(to_hex((stage_3_percent / 100.0 * 255)::int), 2, '0') ||
              '00' AS stage_3_color,
              stage_4,
              stage_4_percent,
              '#' ||
              lpad(to_hex(((100 - stage_4_percent) / 100.0 * 255)::int), 2, '0') ||
              lpad(to_hex((stage_4_percent / 100.0 * 255)::int), 2, '0') ||
              '00' AS stage_4_color
       FROM (
              SELECT group_number,
                     title_from,
                     title_to,
                     total,
                     stage_2,
                     stage_2 * 100 / total AS stage_2_percent,
                     stage_3,
                     stage_3 * 100 / total AS stage_3_percent,
                     stage_4,
                     stage_4 * 100 / total AS stage_4_percent
              FROM (
                     SELECT group_number,
                            min(title)                                        AS title_from,
                            max(title)                                        AS title_to,
                            count(1)                                          AS total,
                            count(1) FILTER ( WHERE "type" IS NOT NULL)       AS stage_2,
                            count(1) FILTER ( WHERE parent_id IS NOT NULL)    AS stage_3,
                            count(1) FILTER ( WHERE leaves_count IS NOT NULL) AS stage_4
                     FROM (
                            SELECT ser.i::text                                                            AS title,
                                   CASE WHEN ser.i % 10 < 10 - ser.i / 10 THEN 'type_123' END             AS "type",
                                   CASE WHEN ser.i % 10 < 10 - 2 * ser.i / 10 THEN 'parent_id_123' END    AS parent_id,
                                   CASE WHEN ser.i % 10 < 10 - 3 * ser.i / 10 THEN 'leaves_count_123' END AS leaves_count,
                                   ntile(_groups_count) OVER ()                                                      AS group_number
                            FROM generate_series(0, 9999) ser(i)
                          ) t
                     GROUP BY t.group_number
                   ) tt
            ) ttt
     ) tttt;
$$ LANGUAGE SQL;

/*
 SELECT public.get_filling_stats(
       _groups_count := 10
 );
  */