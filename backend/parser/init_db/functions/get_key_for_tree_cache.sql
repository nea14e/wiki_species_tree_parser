CREATE FUNCTION public.get_key_for_tree_cache(_language_key1 text, _language_key2 text)
    RETURNS text
    IMMUTABLE
    COST 1
AS
$$
    SELECT _language_key1 || '_' || coalesce(_language_key2, 'null');
$$
    LANGUAGE sql;