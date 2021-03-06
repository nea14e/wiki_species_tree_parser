<h1>Биологическая систематика видов / Biological systematics</h1>

Особенности:

0. Это **просмотрщик** данных из Викивидов и Википедии в удобном виде.

1. **Более 100 000 видов** - те самые, которые есть на Викивидах.

2. Просмотр в виде дерева **с фотографиями**.

3. Данные и фотографии берутся как с Викивидов, так и с Википедий разных языков,
   поэтому здесь данных больше, чем на Википедии любого языка.
   
4. **Мультиязычность,** возможны все языки, какие есть на Википедиях разных стран. В том числе **двуязычие и латынь.**




<h2>Дерево видов</h2>

(Для разработки используются тестовые данные; в данный момент начат парсинг Викивидов и Википедий разных языков)

![Дерево видов](Tree.png?raw=true "Title")

![Дерево видов](Search.png?raw=true "Title")




<h2>Видео</h2>

TODO снять видео по проекту вообще (учитывая, что он почти сделан)

Админка - управление задачами парсера

(Щёлкните на картинку, чтобы смотреть видео на сайте YouTube)
[![Админка - управление задачами парсера - смотреть видео](Videos-admin-parser_tasks.png?raw=true "Title")](https://youtu.be/pciVjlwQ92Q)




<h2>Возможности веб-приложения</h2>

**Разделы:**

- Совет дня (с него начинается навигация)
- Собственно дерево.
  - Возможность показа названий на языке пользователя, на латыни или обоих языках
  - Расрытие/сворачивание элементов, переход к начальному виду. Сначала показаны первые несколько уровней полностью.
  - Переход к чтению Википедии
  - Поиск в Google
  - Поделиться ссылками с друзьями
- Поиск по названию. Использует начало названия вида на языке пользователя либо на латыни.
- Об авторах

**Админка**

В адрес как параметр запроса после `?` добавьте `admin`.
Чуть ниже кнопок навигации откроется поле для ввода пароля.
Введите пароль - откроется панель навигации админа и окно "Задачи БД".
Правильность пароля проверяется при каждом сетевом запросе администратора,
таким как загрузка данных, их сохранение и так далее.
Пароль остаётся запомненным всё время, пока данная вкладка открыта. По кнопке выхода можно стереть свой пароль.

- Управление задачами парсера:
  - Создание, редактирование, дублирование, удаление задач парсера всех видов
  - Запуск, пауза/остановка
  - Автоматический перезапуск или продолжение задач
    - на случай падения сервера (ожидаются задачи длиной в месяц и более)
    - для автоматического запуска задачи миграции БД при обновлении директории проекта через Git
  - Просмотр логов задач
- Управление админ-пользователями (которые будут вносить советы и переводы прямо через интерфейс сайта)

**TODO:**
- Веб-интерфейс админа для удобства перевода на разные языки (управление пользователями-переводчиками уже готово)
- и для отслеживания статистики парсинга в разрезе записей БД (а не только в разрезе задач, как на вкладке задач сейчас).
- Закладки (хранятся в Куки с разрешения пользователя; на сервер ничего не отправляется)
- Выбор языка и второго языка пользователем вручную (двуязычие уже поддерживается, но сейчас первый всегда определяется автоматически, а второй - всегда латынь)
- другое (подробнее см. в TODO.txt)



<h2>Инструкция по развёртыванию</h2>

**База данных**

Postgres 9.6+

Создавать БД или иметь её дамп не надо, достаточно запустить 0 этап парсера:
```
python3.6 ./parser/wiki_parser.py test 0
```
для создания тестовой БД с тестовыми данными на сервере, координаты которого указаны в файле `parser/db_functions.py`,
или
```
python3.6 ./parser/wiki_parser.py no_test 0
```
для создания пустой "боевой" БД.

После этого через веб-интерфейс администратора можно создать
в БД задачи по миграции (stage = 0), которые будут запускаться
автоматически при каждом запуске бэкенда.
Это полезно для лёгкого обновления БД при обновлении проекта через Git -
достаточно перезапустить сервер, и все миграции будут применены.
При миграциях никакие "боевые" данные не удаляются. 

**Парсер**

Парсером для наполнения базы данных можно полностью управлять через веб-интерфейс админки,
в разделе админки Задачи БД.

**Бэкенд**

- Установите python3.6
- Установите pip для python3.6
- Для удобства можно создать виртуальную среду в корневой папке проекта,
чтобы установленные зависимости не перемещивались.
- Установите все пакеты для python, указанные в файле requirements.txt:
`pip3 install -r requirements.txt`
- Создайте файл `Config.py` на основе `Config_EXAMPLE.py`.
 Поменяйте в нём пароль суперадмина `BACKEND_ADMIN_PASSWORD` и секретный ключ бэкенда `BACKEND_SECRET_KEY`.
 Настройте там же координаты своей базы данных,
 установите `IS_DEBUG`, `BACKEND_IS_USE_TEST_DB`.

**Фронтенд**

- Установите Angular 2+
(Это жесть какая-то... я вроде поставил Node.js, Angular CLI но никак не мог их запустить, а потом просто поставил себе WebStorm, который нашёл и запустил их сам.)
- Установите пакеты, используемые во фронтенде
- Настройте адрес бэкенда в файле environment.ts