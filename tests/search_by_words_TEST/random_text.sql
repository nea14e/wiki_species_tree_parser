CREATE OR REPLACE FUNCTION public.random_text(_language_key text, _length int DEFAULT 5)
  RETURNS text
  LANGUAGE PLPGSQL
AS
$$
DECLARE
  _possible_chars text;
  output          text;
  _i              int;
  _pos            int;
BEGIN
  _possible_chars = CASE _language_key
                      WHEN 'en' THEN '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                      WHEN 'ru' THEN '0123456789ФБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯ'
    END;

  output = '';
  FOR _i IN 1.._length
    LOOP
      _pos := public.random_range(1, length(_possible_chars));
      output := output || substr(_possible_chars, _pos, 1);
    END LOOP;

  RETURN output;
END;
$$;
