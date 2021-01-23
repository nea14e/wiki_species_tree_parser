CREATE OR REPLACE FUNCTION public.check_right(user_password text, right_r text)
  RETURNS text
  STABLE
  LANGUAGE SQL
AS
$$
SELECT CASE
         WHEN NOT EXISTS(
             SELECT 1
             FROM public.admin_users
             WHERE password = user_password
           ) THEN 'admin_error_wrong_password'
         WHEN NOT EXISTS(
             SELECT 1
             FROM public.admin_users
             WHERE password = user_password
               AND is_blocked = FALSE
           ) THEN 'admin_error_blocked'
         WHEN NOT EXISTS(
             SELECT 1
             FROM public.admin_users
                    CROSS JOIN jsonb_array_elements(rights_list) i(item)
             WHERE password = user_password
               AND is_blocked = FALSE
               AND (i.item ->> 'r') = right_r
           ) THEN 'admin_error_no_right'
         ELSE 'OK'
         END;
$$;