DO
$$
BEGIN
    IF NOT EXISTS(SELECT 1
                  FROM pg_type
                  WHERE typname = 'parent_mode') THEN
                      
        CREATE TYPE parent_mode AS ENUM ('regular', 'named_only', 'all');
        
    END IF;
END;
$$
LANGUAGE plpgsql;