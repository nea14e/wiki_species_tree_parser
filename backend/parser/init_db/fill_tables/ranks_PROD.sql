TRUNCATE public.ranks;

-- это вся Биота
INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Imperium', -8290, '{
  "ru": "Наддомен"
}', FALSE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Domain', -8300, '{
  "ru": "Домен"
}', FALSE);

-- домен = надцарство
INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Supraregnum', -8301, '{
  "ru": "Надцарство"
}', FALSE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Realm', -8400, '{
  "ru": "Реалм"
}', FALSE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Subrealm', -8410, '{
  "ru": "Субреалм"
}', FALSE);

-- надцарство выше
INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Regnum', -8500, '{
  "ru": "Царство"
}', TRUE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Subregnum', -8510, '{
  "ru": "Подцарство"
}', FALSE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Infraregnum', -8520, '{
  "ru": "Инфрацарство"
}', FALSE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Parvregnum', -8530, '{
  "ru": "Парвцарство"
}', FALSE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Supraphylum', -8590, '{
  "ru": "Надтип"
}', FALSE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Phylum', -8600, '{
  "ru": "Тип"
}', TRUE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Subphylum', -8610, '{
  "ru": "Подтип"
}', FALSE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Infraphylum', -8620, '{
  "ru": "Инфратип"
}', FALSE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Supradivisio', -8690, '{
  "ru": "Надотдел"
}', FALSE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Divisio', -8700, '{
  "ru": "Отдел"
}', FALSE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Subdivisio', -8710, '{
  "ru": "Подотдел"
}', FALSE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Megaclassis', -8780, '{
  "ru": "Мегакласс"
}', FALSE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Supraclassis', -8790, '{
  "ru": "Надкласс"
}', FALSE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Classis', -8800, '{
  "ru": "Класс"
}', TRUE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Subclassis', -8810, '{
  "ru": "Подкласс"
}', FALSE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Infraclassis', -8820, '{
  "ru": "Инфракласс"
}', FALSE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Parvclassis', -8830, '{
  "ru": "Парвкласс"
}', FALSE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Supralegio', -8890, '{
  "ru": "Надлегион"
}', FALSE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Legio', -8900, '{
  "ru": "Легион"
}', FALSE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Sublegio', -8910, '{
  "ru": "Подлегион"
}', FALSE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Infralegio', -8920, '{
  "ru": "Инфралегион"
}', FALSE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Megacohors', -8980, '{
  "ru": "Мегакогорта"
}', FALSE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Supracohors', -8990, '{
  "ru": "Надкогорта"
}', FALSE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Cohors', -9000, '{
  "ru": "Когорта"
}', FALSE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Subcohors', -9010, '{
  "ru": "Подкогорта"
}', FALSE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Infracohors', -9020, '{
  "ru": "Инфракогорта"
}', FALSE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Magnordo', -9060, '{
  "ru": "Магнотряд"
}', FALSE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Supraordo', -9070, '{
  "ru": "Надотряд"
}', FALSE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Grandordo', -9080, '{
  "ru": "Грандотряд"
}', FALSE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Mirordo', -9090, '{
  "ru": "Миротряд"
}', FALSE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Ordo', -9100, '{
  "ru": "Отряд"
}', TRUE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Subordo', -9110, '{
  "ru": "Подотряд"
}', FALSE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Infraordo', -9120, '{
  "ru": "Инфраотряд"
}', FALSE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Parvordo', -9130, '{
  "ru": "Парвотряд"
}', FALSE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Suprafamilia', -9280, '{
  "ru": "Надсемейство"
}', FALSE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Epifamilia', -9290, '{
  "ru": "Эписемейство"
}', FALSE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Familia', -9300, '{
  "ru": "Семейство"
}', TRUE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Subfamilia', -9310, '{
  "ru": "Подсемейство"
}', FALSE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Infrafamilia', -9320, '{
  "ru": "Инфрасемейство"
}', FALSE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Supratribus', -9390, '{
  "ru": "Надтриба"
}', FALSE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Tribus', -9400, '{
  "ru": "Триба"
}', FALSE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Subtribus', -9410, '{
  "ru": "Подтриба"
}', FALSE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Infratribus', -9420, '{
  "ru": "Инфратриба"
}', FALSE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Genus', -9500, '{
  "ru": "Род"
}', TRUE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Nothogenus', -9501, '{
  "ru": "Notho-род"
}', FALSE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Subgenus', -9510, '{
  "ru": "Подрод"
}', FALSE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Suprasectio', -9590, '{
  "ru": "Надсекция"
}', FALSE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Sectio', -9600, '{
  "ru": "Секция"
}', FALSE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Subsectio', -9610, '{
  "ru": "Подсекция"
}', FALSE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Series', -9700, '{
  "ru": "Ряд"
}', FALSE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Subseries', -9710, '{
  "ru": "Подряд"
}', FALSE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Supraspecies', -9790, '{
  "ru": "Надвид"
}', FALSE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('†Species', -9799, '{
  "ru": "Вымерший вид"
}', TRUE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Species', -9800, '{
  "ru": "Вид"
}', TRUE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Nothospecies', -9801, '{
  "ru": "Notho-вид"
}', FALSE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Subspecies', -9810, '{
  "ru": "Подвид"
}', FALSE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Nothosubspecies', -9811, '{
  "ru": "Notho-подвид"
}', FALSE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Varietas', -9900, '{
  "ru": "Разновидность"
}', FALSE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Nothovarietas', -9901, '{
  "ru": "Notho-разновидность"
}', FALSE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Subvarietas', -9910, '{
  "ru": "Подразновидность"
}', FALSE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Forma', -10000, '{
  "ru": "Форма"
}', FALSE);

INSERT INTO public.ranks (type, "order", titles_by_languages, is_regular)
VALUES ('Subforma', -10010, '{
  "ru": "Подформа"
}', FALSE);
