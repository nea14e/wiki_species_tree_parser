TRUNCATE public.ranks;

-- это вся Биота
INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Imperium', -8290, '{"ru": "наддомен"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Domain', -8300, '{"ru": "домен"}');

-- домен = надцарство
INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Supraregnum', -8301, '{"ru": "надцарство"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Realm', -8400, '{"ru": "реалм"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Subrealm', -8410, '{"ru": "субреалм"}');

-- надцарство выше
INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Regnum', -8500, '{"ru": "царство"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Subregnum', -8510, '{"ru": "подцарство"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Infraregnum', -8520, '{"ru": "инфрацарство"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Parvregnum', -8530, '{"ru": "парвцарство"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Supraphylum', -8590, '{"ru": "надтип"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Phylum', -8600, '{"ru": "тип"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Subphylum', -8610, '{"ru": "подтип"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Infraphylum', -8620, '{"ru": "инфратип"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Supradivisio', -8690, '{"ru": "надотдел"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Divisio', -8700, '{"ru": "отдел"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Subdivisio', -8710, '{"ru": "подотдел"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Megaclassis', -8780, '{"ru": "мегакласс"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Supraclassis', -8790, '{"ru": "надкласс"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Classis', -8800, '{"ru": "класс"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Subclassis', -8810, '{"ru": "подкласс"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Infraclassis', -8820, '{"ru": "инфракласс"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Parvclassis', -8830, '{"ru": "парвкласс"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Supralegio', -8890, '{"ru": "надлегион"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Legio', -8900, '{"ru": "легион"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Sublegio', -8910, '{"ru": "подлегион"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Infralegio', -8920, '{"ru": "инфралегион"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Megacohors', -8980, '{"ru": "мегакогорта"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Supracohors', -8990, '{"ru": "надкогорта"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Cohors', -9000, '{"ru": "когорта"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Subcohors', -9010, '{"ru": "подкогорта"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Infracohors', -9020, '{"ru": "инфракогорта"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Magnordo', -9060, '{"ru": "магнотряд"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Supraordo', -9070, '{"ru": "надотряд"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Grandordo', -9080, '{"ru": "грандотряд"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Mirordo', -9090, '{"ru": "миротряд"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Ordo', -9100, '{"ru": "отряд"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Subordo', -9110, '{"ru": "подотряд"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Infraordo', -9120, '{"ru": "инфраотряд"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Parvordo', -9130, '{"ru": "парвотряд"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Suprafamilia', -9280, '{"ru": "надсемейство"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Epifamilia', -9290, '{"ru": "эписемейство"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Familia', -9300, '{"ru": "семейство"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Subfamilia', -9310, '{"ru": "подсемейство"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Infrafamilia', -9320, '{"ru": "инфрасемейство"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Supratribus', -9390, '{"ru": "надтриба"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Tribus', -9400, '{"ru": "триба"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Subtribus', -9410, '{"ru": "подтриба"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Infratribus', -9420, '{"ru": "инфратриба"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Genus', -9500, '{"ru": "род"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Nothogenus', -9501, '{"ru": "notho-род"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Subgenus', -9510, '{"ru": "подрод"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Suprasectio', -9590, '{"ru": "надсекция"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Sectio', -9600, '{"ru": "секция"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Subsectio', -9610, '{"ru": "подсекция"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Series', -9700, '{"ru": "ряд"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Subseries', -9710, '{"ru": "подряд"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Supraspecies', -9790, '{"ru": "надвид"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('†Species', -9799, '{"ru": "вымерший вид"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Species', -9800, '{"ru": "вид"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Nothospecies', -9801, '{"ru": "notho-вид"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Subspecies', -9810, '{"ru": "подвид"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Nothosubspecies', -9811, '{"ru": "notho-подвид"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Varietas', -9900, '{"ru": "разновидность"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Nothovarietas', -9901, '{"ru": "notho-разновидность"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Subvarietas', -9910, '{"ru": "подразновидность"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Forma', -10000, '{"ru": "форма"}');

INSERT INTO public.ranks (type, "order", titles_by_languages)
VALUES ('Subforma', -10010, '{"ru": "подформа"}');
