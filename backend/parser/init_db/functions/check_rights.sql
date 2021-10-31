CREATE OR REPLACE FUNCTION public.check_rights(user_password text, right_rs_list json)
  RETURNS text
  STABLE
  LANGUAGE SQL
AS
$$
-- Проверяет, что у пользователя есть хотя бы одно из прав из списка.
-- Выдаёт текст 'OK' либо сообщение с ключом словаря переводов для текста ошибки.
-- !!! На наличие прав суперпользователя не проверяется, это нужно на бэкенде.
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
               AND (i.item ->> 'r') IN (SELECT json_array_elements_text(right_rs_list))
           ) THEN 'admin_error_no_right'
         ELSE 'OK'
         END;
$$;