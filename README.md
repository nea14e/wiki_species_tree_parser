<h1>Биологическая систематика видов / Biological systematics</h1>

Особенности:
- несколько сотен тысяч видов - те самые, которые есть на Викивидах;
- многие - с фотографиями, взятыми с Викивидов или с разных Википедий;
- языки все, какие есть на Википедиях разных стран.

<h2>Общая подготовка</h2>

- Установите python3.6
- Установите pip для python
- Для удобства можно создать виртуальную среду в корневой папке проекта,
чтобы установленные зависимости не перемещивались.
- Установите все пакеты для python, указанные в файле requirements.txt:

`pip3 install -r requirements.txt`

- Создайте файл с ключом для Python Django по адресу:

`backend/backend/secret_key.txt`

- Установите Angular 2+

TODO

- Файл конфига

Создайте файл `config.py` в корне проекта путём копирования файла `config_EXAMPLE.py`.
Настройте в нём:
1. координаты базы данных Postgres
2. придумайте свой `BACKEND_SECRET_KEY`. Это просто некий ключ для работы бэкенда Django.
3. придумайте свой `BACKEND_ADMIN_URL_PREFIX`. С этого префикса будут начинаться URL, предназначенные для обслуживания парсера/базы данных. Запросы по этим URL могут надолго повесить базу.

Для отладки используйте флажок `IS_DEBUG = True`.
По умолчанию бэкенд использует тестовую базу данных - флажок `BACKEND_IS_USE_TEST_DB = True`.

<h2>Парсер</h2>

Консольное приложение на Python, загружающее с Викивидов данные по животным (адреса страниц, фотографий, названия видов, систематику) в базу данных.
Составляет базу данных для веб-приложения, показывающего дерево видов животных с фотографиями.

Запускайте через параметры командной строки, находясь в папке `parser`:

- Инициализация тестовой базы

В этом случае достаточно одной команды

`python3.6 wiki_parser.py 0 test`

и делать последующие шаги парсера не нужно.

На сервере создастся база данных `lifetree_test`, если такой ещё нет.
Если она есть, то содержимое таблиц будет приведено в соответствие тестовому примеру.
Можно подключить бэкенд к тестовой базе, изменив в файле `config.py` флажок `BACKEND_IS_USE_TEST_DB = True`.

- Для 0 этапа - инициализации базы:

`python3.6 wiki_parser.py 0`

Добавьте слово `test` через пробел для создания тестовой базы (при этом тестовая база не требует дальнеших этапов для наполнения).

- Вы можете добавлять языки (переводы интерфейса и индексы для быстрого поиска данных на этих языка).
Для этого вручную отредактируйте скрипт заполнения таблицы языков,
находящийся в папке проекта по адресу `init_db/fill_tables/known_languages_ANY.sql`,
и запустите инициализацию базы повторно. Если вы просто отредактируете таблицу `public.known_languages` вручную,
то при последующей инициализации базы ваши изменения будут потеряны. 
И при инициализации базы, и при ручном редактировании индексы для быстрого поиска будут автоматически приведены в соответствие полям `lang_key` из этой таблицы.
Чтобы индексы работали, в качестве значений `lang_key` используйте только префиксы доменного имени Википедии нужного языка,
например, для английского - `'en'`, потому что домен английской Википедии - `https://en.wikipedia.org/`.
 
- Для 1 этапа - составления списка для будущего парсинга:

`python3.6 wiki_parser.py 1 [from_title] [to_title] [proxy_string]`

Опциональные параметры указаны в квадратных скобках.

`from_title, to_title` - (опциональны) - заголовки на латыни С по ПО который будет производиться составление списка видов.
Здесь заголовки - на латыни, как в Викивидах.

Например, команда

`python3.6 wiki_parser.py 1 Aa K`

будет составлять список в пределах от `Aa` до `K`, не включая верхнуюю границу.

На этом этапе создаются полупустые записи в таблице `public.list` базы данных. Названия, по которым берутся пределы, находятся в колонке `title` этой таблицы.
Все записи должны быть добавлены в базу до этапа 2 - на этапе 2 они будут лишь обновляться, но не добавляться.

Ожидается, что составление списка будет занимать порядка одних суток. Можно использовать несколько экземпляров программы
и (опционально) прокси, задавая `proxy_string` в формате

`"протокол://адрес:порт@логин:пароль"`
 
 или
 
 `"протокол://адрес:порт"`

- Для 2 этапа - получения деталей по списку:

`python3.6 wiki_parser.py 2 ["True" начать от последнего распарсенного / "False"] [where_фильтр_на_список_как_в_SQL] [proxy_string]`

Например,

`python3.6 wiki_parser.py 2 True "title >= 'Aa' AND title < 'E'"`

Ожидается, что работа в одном потоке на этом этапе займёт несколько месяцев. Поэтому можно запускать несколько экземпляров программы,
задавая им разные интервалы в том же формате, как пишется `WHERE` в SQL. Например,

`python3.6 wiki_parser.py 2 True "title >= 'Aa' AND title < 'E'" "https://my-proxy-1:8080@login:password"`

`python3.6 wiki_parser.py 2 True "title >= 'E' AND title < 'K'" "https://my-proxy-2:8080@login:password"`

`python3.6 wiki_parser.py 2 True "title >= 'K' AND title < 'R'" "https://my-proxy-3:8080@login:password"`

...
 
При этом выражение SQL нужно взять в двойные кавычки, чтобы оно считалось одним аргументом, так как оно содержит внутри себя пробелы.

Прокси опциональны и указываются последним аргументом при запуске в том же формате, как описано на этапе 1.

Здесь если булевый флаг равен `True`, то программа отсчитывает последнюю распарсенную запись в пределах заданного интервала
и начинает с неё, даже если на заданном интервале остались нераспарсенные промежутки. Это полезно, так как в реальности
многие одиночные записи по различным причинам не могут быть распарсены, хотя попали в список на этапе 1 - 
так при повторном запуске этапа 2 на том же интервале не тратится лишнее время на повторные попытки их распарсить.

Если же тот флаг равен `False`, то программа будет пытаться распарсить все ещё не распарсенные записи на заданном интервале.
Это полезно, если вдруг по каким-то причинам в конце этого интервала взялись распарсенные записи - тогда при `True`
программа начинала бы с их конца и поэтому пропущенный интервал оставался бы нетронутым.

Используйте `True` во время парсинга, чтобы не терять время при перезапуске программы, а `False` используйте только чтобы
проверить, что не осталось таких пропущенных интервалов, и распарсить их, если они есть - повторно пройтись по всем интервалам, когда парсинг в целом уже завершён.

- Для 3 этапа - построения древовидной структуры:

`python3.6 wiki_parser.py 3 [where_фильтр_на_список_как_в_SQL]`

Этот этап может занять несколько часов.
Можно использовать несколько экземпляров программы на разных интервалах имён (точно так же, как описано на этапе 2).

Этот этап можно частично выполнить до завершения этапа 2, чтобы посмотреть промежуточные результаты.
При этом он будет использовать только те записи, которые к тому моменту будут уже распарсены на этапе 2,
а когда этап 2 пройдут все записи, то нужно будет просто вызвать этот этап снова для уже полного построения дерева и ничего при этом не сломается.

Эта команда не загружает ничего по сети.

- Для 4 этапа - подсчёта количества видов в каждом узле дерева:

`python3.6 wiki_parser.py 4`

Этот запрос в базу данных может выполняться очень долго либо вообще упасть.
В последнем случае этот этап нужно будет переработать.
Просто так добавить сюда `[where_фильтр_на_список_как_в_SQL]` не получилось,
так как он реализован через хранимку. Но можно переделать его с хранимки
на отдельные запросы, кидаемые из питона - тогда каждый запрос будет выполняться
в своей транзакции и есть шансы избежать переполнения.

Этот этап можно выполнить до завершения этапа 2, чтобы посмотреть промежуточные результаты с заполненными числами количеств видов.
Для этого сначала вызовите этап 3, а затем этот этап.
При этом этот этап будет использовать только те записи, которые к тому моменту будут уже распарсены на этапе 2 и на этапе 3,
а когда этап 2 пройдут все записи, то нужно будет просто вызвать этапы 3 и 4 снова и ничего при этом не сломается.

Эта команда не загружает ничего по сети.

- Отдельным этапом - добавление переводов на язык по списку

`python3.6 wiki_parser.py parse_language <lang_key> ["True" начать от последнего распарсенного / "False"] [where_фильтр_на_список_как_в_SQL] [proxy_string]`

Эта команда во всём аналогична команде этапа 2, её так же можно запускать на нескольких интервалах
названий видов и так же можно использовать прокси, только в начале команды обязательно указывается ключ языка `<lang_key>`.
Ключ языка обязательно берётся из доменного имени Википедии этого языка.
Например, если русская Википедия имеет домен `https://ru.wikipedia.org/`, то ключ языка равен `ru`.

Например,

`python3.6 wiki_parser.py parse_language ru True "title >= 'Aa' AND title < 'E'"`

На этом этапе также добавляются картинки из Википедий, если ранее не было найдено никакой картинки.

Этот этап (добавление переводов) выполняется только для тех записей, которые уже прошли этап 2.
Этапы 3 и 4 на него не оказывают никакого влияния.

<h2>Веб-приложение: бэкенд</h2>

`python3.6 manage.py runserver` (из папки `backend`)

Запускается за несколько секунд. В консоли должно появиться что-то вида

`July 12, 2020 - 21:04:47`

`Django version 3.0.8, using settings 'backend.settings'`

`Starting development server at http://127.0.0.1:8000/`

`Quit the server with CTRL-BREAK.`

(Обратите внимание на порт, указанный по умолчанию.)

Изменить используемую бэкендом базу данных с `lifetree` на `lifetree_test`
можно в файле `config.py`, установив или сбросив флажок `BACKEND_IS_USE_TEST_DB`.

Чтобы проверить работоспособность сервера, можно перейти по напечатанной там ссылке http://127.0.0.1:8000/ -
в ответ должен придти JSON вида

`{"title": "This is wiki_species_tree_parser API-backend", "django_state": "Ok", "db_state": "Db is online", "info": "Please read README for more abilities."}`

Возможности backend:
- Проверка работоспособности:
  - GET http://127.0.0.1:8000/ или GET http://127.0.0.1:8000/check
- API для frontend (URL-адреса начинаются с префикса `API/`):
  - GET http://127.0.0.1:8000/api/get_tree_default - выдаёт дерево с видом по умолчанию (первые три уровня целиком). Нужно для первого открытия страницы по URL по умолчанию.
  - GET http://127.0.0.1:8000/api/get_tree_by_id/222 - выдаёт дерево, раскрытое на записи с нужным id `222` (уровни до него и все его прямые потомки на разных уровнях). Нужно, когда страница загружается напрямую по URL определённого элемента.
  - GET http://127.0.0.1:8000/api/get_childes_by_id/222 - выдаёт дочернюю часть дерева для записи с нужным id `222` (все его прямые потомки на разных уровнях). Нужно, когда пользователь раскрывает часть дерева.
  - GET http://127.0.0.1:8000/api/search_by_words/bbx/1 - поиск по названию `bbx`. Запрос должен быть на языке браузера пользователя либо на латыни. Ищется по началу названия. Выдаёт список. Для подгрузки списка второй параметр - отступ, в примере он равен `1`.
- Для администратора (URL-адреса начинаются с префикса администратора, так как выполнение этих команд может отнять много ресурсов у БД и поэтому их надо было спрятать):
  - GET http://127.0.0.1:8000/<admin_url_prefix>/count_1 - подсчитать количество записей видов в базе данных (все, прошедшие этап 1 парсинга) 
  - GET http://127.0.0.1:8000/<admin_url_prefix>/count_2 - подсчитать количество распарсенных видов в базе данных (все, прошедшие этап 2 парсинга) 
  - GET http://127.0.0.1:8000/<admin_url_prefix>/count_3 - подсчитать количество видов, подключенных куда-либо в дереве в базе данных (все, прошедшие этап 3 парсинга) 




<h2>Веб-приложение: фронтэнд</h2>
TODO