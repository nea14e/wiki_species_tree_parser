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

`python3.6 wiki_parser.py 1 [from_title] [to_title]`
Здесь заголовки - на латыни, как в Викивидах; берутся из поля `title` таблицы `public.list`.

- Для 2 этапа - получения деталей по списку:

`python3.6 wiki_parser.py 2 ["True" начать от последнего распарсенного / "False"] [where_фильтр_на_список_как_в_SQL]`

- Для 3 этапа - построения древовидной структуры:

`python3.6 wiki_parser.py 3 [where_фильтр_на_список_как_в_SQL]`

- Для 4 этапа - подсчёта количества видов в каждом узле дерева:

`python3.6 wiki_parser.py 4`

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
  - TODO 
- Для администратора (URL-адреса начинаются с префикса администратора):
  - Подсчитать количество записей видов в базе данных: `https://<domen>/<admin_url_prefix>/get_count` 

<h2>Веб-приложение: фронтэнд</h2>
TODO