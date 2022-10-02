CREATE OR REPLACE FUNCTION public.percent_of_to_color(_number bigint, _max_number bigint)
  RETURNS text
  IMMUTABLE
AS
$$
  -- Выдаёт цвет в формате '#ff00ff' (текст) согласно проценту, который занимает _number в _max_number
DECLARE
  _percent int;
BEGIN
  _percent = public.percent_of(_number, _max_number);

  RETURN '#' ||
         lpad(to_hex(((100 - _percent) / 100.0 * 255)::int), 2, '0') ||
         lpad(to_hex((_percent / 100.0 * 255)::int), 2, '0') ||
         '00';
END;
$$ LANGUAGE 'plpgsql';