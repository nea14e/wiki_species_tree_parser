CREATE OR REPLACE FUNCTION public.get_languages_list() 
    RETURNS json
    STABLE
AS
$$
    SELECT jsonb_agg(t)::json
    FROM (SELECT kl.lang_key,
                 kl.comment,
                 kl.is_main_for_admins
          FROM public.known_languages kl
          ORDER BY kl.lang_key) t;
$$
    LANGUAGE sql;

-- SELECT public.get_languages_list(); 