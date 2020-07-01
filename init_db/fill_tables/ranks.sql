-- noinspection SqlWithoutWhere
DELETE FROM public.ranks;

INSERT INTO public.ranks (type, "order")
VALUES
       ('1st', -10),
       ('2nd', -20),
       ('3rd', -30),
       ('4th', -40),
       ('5th', -50),
       ('6th', -60);