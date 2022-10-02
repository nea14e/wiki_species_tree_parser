CREATE OR REPLACE FUNCTION public.percent_of(_number bigint, _max_number bigint)
  RETURNS int
  IMMUTABLE
AS
$$
  -- Рассчитывает процент, который занимает _number в _max_number
BEGIN
  RETURN _number * 100 / _max_number;
END;
$$ LANGUAGE 'plpgsql';