TRUNCATE public.ranks;
/*
-- это вся Биота
INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Наддомен', 'Imperium', -8290, '{
  "ru": "Наддомен"
}', FALSE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Домен', 'Domain', -8300, '{
  "ru": "Домен"
}', FALSE);

-- домен = надцарство
INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Надцарство', 'Supraregnum', -8301, '{
  "ru": "Надцарство"
}', FALSE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Реалм', 'Realm', -8400, '{
  "ru": "Реалм"
}', FALSE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Субреалм', 'Subrealm', -8410, '{
  "ru": "Субреалм"
}', FALSE);
 */
-- надцарство выше
INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Царство', 'Regnum', -8500, '{
  "ru": "Царство"
}', TRUE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Подцарство', 'Subregnum', -8510, '{
  "ru": "Подцарство"
}', FALSE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Инфрацарство', 'Infraregnum', -8520, '{
  "ru": "Инфрацарство"
}', FALSE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Парвцарство', 'Parvregnum', -8530, '{
  "ru": "Парвцарство"
}', FALSE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Надтип', 'Supraphylum', -8590, '{
  "ru": "Надтип"
}', FALSE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Тип', 'Phylum', -8600, '{
  "ru": "Тип"
}', TRUE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Подтип', 'Subphylum', -8610, '{
  "ru": "Подтип"
}', FALSE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Инфратип', 'Infraphylum', -8620, '{
  "ru": "Инфратип"
}', FALSE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Надотдел', 'Supradivisio', -8690, '{
  "ru": "Надотдел"
}', FALSE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Отдел', 'Divisio', -8700, '{
  "ru": "Отдел"
}', FALSE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Подотдел', 'Subdivisio', -8710, '{
  "ru": "Подотдел"
}', FALSE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Мегакласс', 'Megaclassis', -8780, '{
  "ru": "Мегакласс"
}', FALSE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Надкласс', 'Supraclassis', -8790, '{
  "ru": "Надкласс"
}', FALSE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Класс', 'Classis', -8800, '{
  "ru": "Класс"
}', TRUE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Подкласс', 'Subclassis', -8810, '{
  "ru": "Подкласс"
}', FALSE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Инфракласс', 'Infraclassis', -8820, '{
  "ru": "Инфракласс"
}', FALSE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Парвкласс', 'Parvclassis', -8830, '{
  "ru": "Парвкласс"
}', FALSE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Надлегион', 'Supralegio', -8890, '{
  "ru": "Надлегион"
}', FALSE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Легион', 'Legio', -8900, '{
  "ru": "Легион"
}', FALSE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Подлегион', 'Sublegio', -8910, '{
  "ru": "Подлегион"
}', FALSE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Инфралегион', 'Infralegio', -8920, '{
  "ru": "Инфралегион"
}', FALSE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Мегакогорта', 'Megacohors', -8980, '{
  "ru": "Мегакогорта"
}', FALSE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Надкогорта', 'Supracohors', -8990, '{
  "ru": "Надкогорта"
}', FALSE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Когорта', 'Cohors', -9000, '{
  "ru": "Когорта"
}', FALSE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Подкогорта', 'Subcohors', -9010, '{
  "ru": "Подкогорта"
}', FALSE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Инфракогорта', 'Infracohors', -9020, '{
  "ru": "Инфракогорта"
}', FALSE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Магнотряд', 'Magnordo', -9060, '{
  "ru": "Магнотряд"
}', FALSE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Надотряд', 'Supraordo', -9070, '{
  "ru": "Надотряд"
}', FALSE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Грандотряд', 'Grandordo', -9080, '{
  "ru": "Грандотряд"
}', FALSE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Миротряд', 'Mirordo', -9090, '{
  "ru": "Миротряд"
}', FALSE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Отряд', 'Ordo', -9100, '{
  "ru": "Отряд"
}', TRUE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Подотряд', 'Subordo', -9110, '{
  "ru": "Подотряд"
}', FALSE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Инфраотряд', 'Infraordo', -9120, '{
  "ru": "Инфраотряд"
}', FALSE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Парвотряд', 'Parvordo', -9130, '{
  "ru": "Парвотряд"
}', FALSE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Надсемейство', 'Suprafamilia', -9280, '{
  "ru": "Надсемейство"
}', FALSE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Эписемейство', 'Epifamilia', -9290, '{
  "ru": "Эписемейство"
}', FALSE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Семейство', 'Familia', -9300, '{
  "ru": "Семейство"
}', TRUE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Подсемейство', 'Subfamilia', -9310, '{
  "ru": "Подсемейство"
}', FALSE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Инфрасемейство', 'Infrafamilia', -9320, '{
  "ru": "Инфрасемейство"
}', FALSE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Надтриба', 'Supratribus', -9390, '{
  "ru": "Надтриба"
}', FALSE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Триба', 'Tribus', -9400, '{
  "ru": ""
}', FALSE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Подтриба', 'Subtribus', -9410, '{
  "ru": "Подтриба"
}', FALSE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Инфратриба', 'Infratribus', -9420, '{
  "ru": "Инфратриба"
}', FALSE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Род', 'Genus', -9500, '{
  "ru": "Род"
}', TRUE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Notho-род', 'Nothogenus', -9501, '{
  "ru": "Notho-род"
}', FALSE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Подрод', 'Subgenus', -9510, '{
  "ru": "Подрод"
}', FALSE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Надсекция', 'Suprasectio', -9590, '{
  "ru": "Надсекция"
}', FALSE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Секция', 'Sectio', -9600, '{
  "ru": "Секция"
}', FALSE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Подсекция', 'Subsectio', -9610, '{
  "ru": "Подсекция"
}', FALSE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Ряд', 'Series', -9700, '{
  "ru": "Ряд"
}', FALSE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Подряд', 'Subseries', -9710, '{
  "ru": "Подряд"
}', FALSE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Надвид', 'Supraspecies', -9790, '{
  "ru": "Надвид"
}', FALSE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Вымерший вид', '†Species', -9799, '{
  "ru": "Вымерший вид"
}', TRUE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Вид', 'Species', -9800, '{
  "ru": "Вид"
}', TRUE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Notho-вид', 'Nothospecies', -9801, '{
  "ru": "Notho-вид"
}', FALSE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Подвид', 'Subspecies', -9810, '{
  "ru": "Подвид"
}', FALSE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Notho-подвид', 'Nothosubspecies', -9811, '{
  "ru": "Notho-подвид"
}', FALSE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Разновидность', 'Varietas', -9900, '{
  "ru": "Разновидность"
}', FALSE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Notho-разновидность', 'Nothovarietas', -9901, '{
  "ru": "Notho-разновидность"
}', FALSE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Подразновидность', 'Subvarietas', -9910, '{
  "ru": "Подразновидность"
}', FALSE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Форма', 'Forma', -10000, '{
  "ru": "Форма"
}', FALSE);

INSERT INTO public.ranks (type, latin, "order", titles_by_languages, is_regular)
VALUES ('Подформа', 'Subforma', -10010, '{
  "ru": "Подформа"
}', FALSE);
