CREATE OR REPLACE FUNCTION public.random_range(INTEGER, INTEGER)
    RETURNS INTEGER
    LANGUAGE SQL
    AS $$
        SELECT ($1 + FLOOR(($2 - $1 + 1) * random() ))::INTEGER;
    $$;