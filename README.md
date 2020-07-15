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

- Создайте файл с ключом,
который будет автоматически добавлен в каждый URL, предназначенный для обслуживания парсера/базы данных.
Например, если ключ будет содержать `abc123`, то URL для просмотра количества записей
в базе данных будет выглядеть как `https://<domen>/abc123/get_count`.
Этот ключ должен содержать только символы, допустимые в URL (желательно просто только буквы и цифры).
Сам файл должен находиться по адресу:

`backend/backend/admin_ulr_prefix.txt`

- Установите Angular 2+

TODO

<h2>Парсер</h2>

Консольное приложение на Python, загружающее с Викивидов данные по животным (адреса страниц, фотографий, названия видов, систематику) в базу данных.
Составляет базу данных для веб-приложения, показывающего дерево видов животных с фотографиями.

Запускайте через параметры командной строки, находясь в папке `parser`:

- Для 0 этапа - инициализации базы:

`python3.6 wiki_parser.py 0 ["test" для тестового наполнения]`

- Вы можете добавлять языки (переводы интерфейса и индексы для быстрого поиска данных на этих языка).
Для этого вручную отредактируйте скрипт заполнения таблицы языков,
находящийся в папке проекта по адресу `init_db/fill_tables/known_languages_ANY.sql`,
и запустите инициализацию базы повторно. Если вы отредактируете таблицу `public.known_languages` вручную,
то при последующей инициализации базы ваши изменения будут потеряны. 
И при инициализации базы, и при ручном редактировании индексы для быстрого поиска будут автоматически приведены в соответствие полям `lang_key` из этой таблицы.
Чтобы индексы работали, в качестве значений `lang_key` используйте только префиксы доменного имени Википедии нужного языка,
например, для английского - `'en'`, потому что домен английской Википедии - `https://en.wikipedia.org/`.
 
- Для 1 этапа - составления списка:

`python3.6 wiki_parser.py 1 [from_title] [to_title] [proxy_string]`
Здесь заголовки - на латыни, как в Викивидах; берутся из поля `title` таблицы `public.list`.

Ожидается, что составление списка будет занимать порядка одних суток. Можно использовать несколько экземпляров программы
и прокси, задавая `proxy_string` в формате

`"протокол://адрес:порт@логин:пароль"`
 
 или
 
 `"протокол://адрес:порт"`

- Для 2 этапа - получения деталей по списку:

`python3.6 wiki_parser.py 2 ["True" начать от последнего распарсенного / "False"] [where_фильтр_на_список_как_в_SQL] [proxy_string]`

Например,

`python3.6 wiki_parser.py 2 False "title >= 'Aa' AND title < 'E'"`

Ожидается, что работа в одном потоке на этом этапе займёт несколько месяцев. Поэтому можно запускать несколько экземпляров программы,
задавая им разные интервалы в том же формате, как пишется `WHERE` в SQL. Например,

`python3.6 wiki_parser.py 2 False "title >= 'Aa' AND title < 'E'" "https://my-proxy-1:8080@login:password"`

`python3.6 wiki_parser.py 2 False "title >= 'E' AND title < 'K'" "https://my-proxy-2:8080@login:password"`

`python3.6 wiki_parser.py 2 False "title >= 'K' AND title < 'R'" "https://my-proxy-3:8080@login:password"`

...
 
При этом выражение SQL нужно взять в двойные кавычки, чтобы оно считалось одним аргументом.

Прокси указываются последним аргументом при запуске в том же формате, как описано на этапе 1.

Здесь если булевый флаг равен `True`, то программа отсчитывает последнюю распарсенную запись в пределах заданного интервала
и начинает с неё, даже если на заданном интервале остались нераспарсенные промежутки. Это полезно, так как в реальности
многие одиночные записи по различным причинам не могут быть распарсены, хотя попали в список на этапе 1 - 
так при повторном запуске этапа 2 на том же интервале не тратится лишнее время на повторные попытки их распарсить.

Если же тот флаг равен `False`, то программа будет пытаться распарсить все ещё не распарсенные записи на заданном интервале.
Это полезно, если вдруг по каким-то причинам в конце этого интервала взялись распарсенные записи - тогда при `True`
программа начинала бы с их конца и поэтому пропущенный интервал оставался бы нетронутым. Используйте `False`, чтобы
проверить, что не осталось таких пропущенных интервалов, и распарсить их, если они есть.

- Для 3 этапа - построения древовидной структуры:

`python3.6 wiki_parser.py 3 [where_фильтр_на_список_как_в_SQL]`

Запрос в базу на обновление всего дерева может занять час времени либо вообще упасть, если там много элементов.
Поэтому используйте несколько запросов на разных интервалах имён (описано на этапе 2).

Этот этап можно выполнить до завершения этапа 2, чтобы посмотреть промежуточные результаты.
При этом он будет использовать только те записи, которые к тому моменту будут уже распарсены на этапе 2,
а когда этап 2 пройдут все записи, то нужно будет просто вызвать этот этап снова и ничего при этом не сломается.

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
Для этого сначала вызовите этап 3.
При этом этап 4 будет использовать только те записи, которые к тому моменту будут уже распарсены на этапе 2 и на этапе 3,
а когда их пройдут все записи, то нужно будет просто вызвать этапы 3 и 4 снова и ничего при этом не сломается.

Эта команда не загружает ничего по сети.

Настройки парсера находятся в константах (названы крупным шрифтом) в начале файлов `parser/wiki_parser.py`
и `parser/db_functions`. Например,

`IS_DEBUG` - задаёт режим отладки для более подробной печати в консоль (пока что ничего больше). Тормозит работу приложения.
`NEXT_PAGE_DELAY` - задаёт интервал отдыха между концом парсинга предыдущей страницы и началом загрузки следующей (в секундах).
Поскольку парсинг страницы Викивидов и связанных с ней Википедий по языкам занимают значительное время, 
реальный интервал между загрузкой предыдущей страницы и следующей будет значительно больше этого числа.  

<h2>Веб-приложение: бэкенд</h2>

`python3.6 manage.py runserver` (из папки `backend`)

Запускается за несколько секунд. В консоли должно появиться что-то вида

`July 12, 2020 - 21:04:47`

`Django version 3.0.8, using settings 'backend.settings'`

`Starting development server at http://127.0.0.1:8000/`

`Quit the server with CTRL-BREAK.`

Обратите внимание на порт, указанный по умолчанию. Настройки Django можно редактировать в файле

`backend/backend/settings.py`

Чтобы проверить работоспособность сервера, можно перейти по напечатанной там ссылке http://127.0.0.1:8000/ -
в ответ должен придти JSON вида

`{"title": "This is wiki_species_tree_parser API-backend", "django_state": "Ok", "db_state": "Db is Ok", "info": "Please read README for more abilities."}`

Возможности backend:
- Проверка работоспособности:
  - GET http://127.0.0.1:8000/ или GET http://127.0.0.1:8000/check
- API для frontend (URL-адреса начинаются с префикса `API/`):
  - GET http://127.0.0.1:8000/api/get_tree_default - выдаёт дерево с видом по умолчанию (первые три уровня целиком)
  - GET http://127.0.0.1:8000/api/get_tree_by_id/222 - выдаёт дерево, раскрытое на записи с нужным id `222` (уровни до него и все его прямые потомки на разных уровнях)
  - GET http://127.0.0.1:8000/api/search_by_words/bbx - поиск по названию `bbx`. Запрос должен быть на языке браузера пользователя либо на латыни. Ищется по началу названия. Выдаёт список.
- Для администратора (URL-адреса начинаются с префикса администратора):
  - GET https://<domen>/<admin_url_prefix>/count_1 - подсчитать количество записей видов в базе данных (все, прошедшие этап 1 парсинга) 
  - GET https://<domen>/<admin_url_prefix>/count_2 - подсчитать количество распарсенных видов в базе данных (все, прошедшие этап 2 парсинга) 
  - GET https://<domen>/<admin_url_prefix>/count_3 - подсчитать количество видов, подключенных куда-либо в дереве в базе данных (все, прошедшие этап 3 парсинга) 

<h2>Веб-приложение: фронтэнд</h2>
TODO