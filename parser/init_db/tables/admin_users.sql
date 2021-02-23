create table public.admin_users
(
	id serial
		constraint admin_users_pk
			primary key,
	description text not null,
	password text not null,
	is_blocked boolean default FALSE not null
);

create unique index admin_users_password_uindex
	on public.admin_users (password);

