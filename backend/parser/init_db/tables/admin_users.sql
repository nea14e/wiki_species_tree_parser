CREATE TABLE public.admin_users
(
  id          serial
    CONSTRAINT admin_users_pk
      PRIMARY KEY,
  description text                  NOT NULL,
  password    text                  NOT NULL,
  rights_list jsonb                 NOT NULL,
  is_blocked  boolean DEFAULT FALSE NOT NULL
);

CREATE UNIQUE INDEX ix_admin_users_password
  ON admin_users (password);
