import json

import django
from django.db import connections
from django.http import JsonResponse

from species_tree_backend.http_headers_parser import get_language_key

from species_tree_backend.db_task_manager import DbTaskManager

from species_tree_backend.rights import RIGHTS
from config import Config
from config_EXAMPLE import Config as ConfigExample


# ====================================
# Собственно для работы приложения
# ====================================

def get_translations(request):  # выдаёт переводы интерфейса пользователя
    accept_language = request.headers['Accept-Language']
    language_key = get_language_key(accept_language)
    conn = connections["default"]
    cur = conn.cursor()
    cur.execute("""
        SELECT public.get_translations(_language_key := %s);
    """, (language_key,))
    db_response = cur.fetchone()[0]
    return JsonResponse(db_response, safe=False)


def get_childes_by_id(request,
                      _id: int):  # выдаёт дочернюю часть дерева для записи с нужным id (все его прямые потомки на разных уровнях)
    accept_language = request.headers['Accept-Language']
    language_key = get_language_key(accept_language)
    conn = connections["default"]
    cur = conn.cursor()
    cur.execute("""
        SELECT public.get_childes_by_id(_id := %s, _language_key := %s);
    """, (_id, language_key,))
    db_response = cur.fetchone()[0]
    return JsonResponse(db_response, safe=False)


def get_tree_by_id(request,
                   _id: int):  # выдаёт дерево, раскрытое на записи с нужным id (уровни до него и все его прямые потомки на разных уровнях)
    accept_language = request.headers['Accept-Language']
    language_key = get_language_key(accept_language)
    conn = connections["default"]
    cur = conn.cursor()
    cur.execute("""
        SELECT public.get_tree_by_id(_id := %s, _language_key := %s);
    """, (_id, language_key,))
    db_response = cur.fetchone()[0]
    return JsonResponse(db_response, safe=False)


def get_tree_default(request):  # выдаёт дерево с видом по умолчанию (первые три уровня целиком)
    accept_language = request.headers['Accept-Language']
    language_key = get_language_key(accept_language)
    conn = connections["default"]
    cur = conn.cursor()
    cur.execute("""
        SELECT public.get_tree_default(_language_key := %s);
    """, (language_key,))
    db_response = cur.fetchone()[0]
    return JsonResponse(db_response, safe=False)


def get_favorites(request):
    body = json.loads(request.body)
    ids = list(body["ids"])

    accept_language = request.headers['Accept-Language']
    language_key = get_language_key(accept_language)
    conn = connections["default"]
    cur = conn.cursor()
    cur.execute("""
        SELECT public.get_favorites(_ids := %s, _language_key := %s);
    """, (ids, language_key,))
    db_response = cur.fetchone()[0]
    return JsonResponse(db_response, safe=False)  # unsafe указывается только для функций БД на языке SQL


def search_by_words(request, words: str, offset: int):
    if len(words) < 3:
        return JsonResponse({
            "Error": "Query for text-search must have at least 3 characters."
        })
    accept_language = request.headers['Accept-Language']
    language_key = get_language_key(accept_language)
    conn = connections["default"]
    cur = conn.cursor()
    cur.execute("""
        SELECT public.search_by_words(_query := %s, _offset := %s, _language_key := %s);
    """, (words, offset, language_key,))
    db_response = cur.fetchone()[0]
    return JsonResponse(db_response, safe=False)  # unsafe указывается только для функций БД на языке SQL


def get_tip_of_the_day(request):
    accept_language = request.headers['Accept-Language']
    language_key = get_language_key(accept_language)
    conn = connections["default"]
    cur = conn.cursor()
    cur.execute("""
        SELECT public.get_tip_of_the_day(_language_key := %s);
    """, (language_key,))
    db_response = cur.fetchone()[0]
    return JsonResponse(db_response, safe=False)  # unsafe указывается только для функций БД на языке SQL


def get_tip_of_the_day_by_id(request, _id: int = None):
    accept_language = request.headers['Accept-Language']
    language_key = get_language_key(accept_language)
    conn = connections["default"]
    cur = conn.cursor()
    cur.execute("""
        SELECT public.get_tip_of_the_day_by_id(_language_key := %s, _id := %s);
    """, (language_key, _id))
    db_response = cur.fetchone()[0]
    return JsonResponse(db_response, safe=False)  # unsafe указывается только для функций БД на языке SQL


# ====================================
# Администрирование через фронтэнд - ОБЩЕЕ
# ====================================

# Это декоратор для всех функций, где надо проверять, имеет ли админ-пользователь такое право.
# Право указывается при использовании декоратора на конкретной функции. Пустой список [] означает требовать,
# чтобы пользователь был супер-админом, пароль которого находится не в БД, а в файле Config.py.
# Супер-админ имеет безусловные права на всё.
# Тело запроса у декорируемой функции должно содержать пароль пользователя.
def check_right_request_decorator(rights: list):  # этот декоратор при каждом своём использовании требует список прав
    def decorator(func):  # декоратор должен вернуть функцию, которая сама принимает на вход декорируемую функцию func()
        def wrapped(*args, **kw):  # вызов декорируемой функции func() будет заменён на вызов этой функции wrapped() с такими же аргументами
            if ConfigExample.BACKEND_SECRET_KEY == Config.BACKEND_SECRET_KEY:
                return JsonResponse({"is_ok": False,
                                     "message": "You forgot to change Config.BACKEND_SECRET_KEY when copied from Config_EXAMPLE!"})
            if ConfigExample.BACKEND_ADMIN_PASSWORD == Config.BACKEND_ADMIN_PASSWORD:
                return JsonResponse({"is_ok": False,
                                     "message": "You forgot to change Config.BACKEND_ADMIN_PASSWORD when copied from Config_EXAMPLE!"})
            request = args[0]
            result = _check_right_request(request, rights)
            if result is not None:
                return result
            else:
                return func(*args, **kw)  # вот тут сам вызов декорируемой функции, а всё предыдущее - её "обёртка"
        return wrapped
    return decorator


def _check_right_request(request, rights: list):
    # noinspection PyBroadException
    try:
        body = json.loads(request.body)
        password = str(body["adminKey"])
        if password == Config.BACKEND_ADMIN_PASSWORD:  # Если это суперадмин, то всё ок, не проверять дальше
            pass
        else:
            if not rights:  # Если требуется только суперадмин
                return JsonResponse({"is_ok": False,
                                     "message_translation_key": "admin_error_super_admin_only",
                                     "message": "Only super-admin have this permission."})
            # Проверяем хранимкой остальные права. Должно быть хотя бы 1 из списка.
            conn = connections["default"]
            cur = conn.cursor()
            cur.execute("""
                SELECT public.check_rights(%s, %s);
            """, (password, json.dumps(rights),))
            db_response = str(cur.fetchone()[0])
            if db_response == 'OK':
                return None
            else:
                return JsonResponse({"is_ok": False,
                                     "message_translation_key": db_response,
                                     "message": "You do not have this permission."})
    except BaseException:
        return JsonResponse(
            {
                "is_ok": False,
                "message": "All admin's requests must be of HTTP POST type with 'adminKey' provided in POST's json object."
            }
        )


# проверка прав внутри
def admin_try_login(request):
    body = json.loads(request.body)
    password = str(body["adminKey"])

    if password == Config.BACKEND_ADMIN_PASSWORD:
        user = {
            "description": "Super-admin",
            "rights_list": [{"r": RIGHTS.SUPER_ADMIN}]
        }
    else:
        conn = connections["default"]
        cur = conn.cursor()
        cur.execute("""
            SELECT json_build_object(
                       'description', description,
                       'rights_list', rights_list,
                       'is_blocked', is_blocked
                     )
            FROM public.admin_users
            WHERE password = %s
            LIMIT 1;
        """, (password,))
        row = cur.fetchone()
        if row is None:
            return JsonResponse({"is_ok": False,
                                 "message_translation_key": "admin_error_wrong_password",
                                 "message": "Wrong password."})
        user = row[0]
        if bool(user["is_blocked"]):
            return JsonResponse({"is_ok": False,
                                 "message_translation_key": "admin_error_blocked",
                                 "message": "This user have been blocked."})
    return JsonResponse(user, safe=False)  # unsafe указывается только для функций БД на языке SQL


# для этого права не нужны
def _get_admin_user_id_by_password_internal(request):
    body = json.loads(request.body)
    password = str(body["adminKey"])

    if password == Config.BACKEND_ADMIN_PASSWORD:
        return None  # указывает на суперпользователя

    conn = connections["default"]
    cur = conn.cursor()
    cur.execute("""
        SELECT id
        FROM public.admin_users
        WHERE password = %s
        LIMIT 1
    """, (
        password,
    ))
    user_id = cur.fetchone()[0]
    if user_id is None:
        raise ValueError('User not found by password!')
    return int(user_id)


# для этого права не нужны
def admin_get_known_languages_all(request):
    conn = connections["default"]
    cur = conn.cursor()
    cur.execute("""
        SELECT COALESCE(json_agg(t ORDER BY t.lang_key), '[]')
        FROM (
               SELECT *
               FROM public.known_languages
             ) t;
    """)
    db_response = cur.fetchone()[0]
    return JsonResponse(db_response, safe=False)  # unsafe указывается только для функций БД на языке SQL


# для этого права не нужны
def admin_get_main_admin_language(request):
    conn = connections["default"]
    cur = conn.cursor()
    cur.execute("""
        SELECT json_build_object(
                    'lang_key', lang_key,
                    'comment', comment
                )
        FROM public.known_languages
        WHERE is_main_for_admins = TRUE
        LIMIT 1;
    """)
    db_response = cur.fetchone()[0]
    return JsonResponse(db_response, safe=False)  # unsafe указывается только для функций БД на языке SQL


# ====================================
# Администрирование через фронтэнд - ЗАДАЧИ БД
# ====================================

MIGRATION_TASK = {
    "id": -1,
    "stage": "0",
    "python_exe": "python3",
    "args": "{}",
    "is_rerun_on_startup": True,
    "is_resume_on_startup": False,
    "is_success": None,
    "last_crash_message": None,
    "is_auto_created": True
}

# Это обычный метод, не API
def startup_start_tasks():
    conn = connections["default"]
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT COALESCE(json_agg(t ORDER BY t.stage, t.id), '[]')
            FROM (
                   SELECT *
                   FROM public.tasks
              ) t;
        """)
        tasks = list(cur.fetchone()[0])
    except django.db.utils.ProgrammingError:
        tasks = []
    tasks.append(MIGRATION_TASK)
    DbTaskManager.get_instance().start_tasks_on_startup(tasks)  # запускаем (точнее, продолжаем) задачи парсинга по умолчанию
    # Это обычный метод, не API


@check_right_request_decorator([RIGHTS.EDIT_DB_TASKS])
def admin_get_tasks(request):
    conn = connections["default"]
    cur = conn.cursor()
    cur.execute("""
        SELECT COALESCE(json_agg(t ORDER BY t.stage, t.id), '[]')
        FROM (
               SELECT *
               FROM public.tasks
          ) t;
    """)
    tasks = list(cur.fetchone()[0])
    tasks.append(MIGRATION_TASK)
    tasks = DbTaskManager.get_instance().get_tasks_states(tasks)  # добавлем к задачам их состояние запущена/не запущена, последние логи
    return JsonResponse(
        {"tasks": tasks, "is_test_db": Config.BACKEND_IS_USE_TEST_DB},
        safe=False
    )  # unsafe указывается только для запросов БД на языке SQL


@check_right_request_decorator([RIGHTS.EDIT_DB_TASKS])
def admin_add_task(request):
    body = json.loads(request.body)
    conn = connections["default"]
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO public.tasks(stage, python_exe, args, is_rerun_on_startup, is_resume_on_startup)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id;
    """, (body["data"]["stage"], body["data"]["python_exe"], json.dumps(body["data"]["args"]), body["data"]["is_rerun_on_startup"], body["data"]["is_resume_on_startup"]))
    task = body["data"]
    task["id"] = int(cur.fetchone()[0])
    if bool(body["data"]["is_launch_now"]):
        DbTaskManager.get_instance().start_one_task(task)  # запускаем задачу
    return JsonResponse({"is_ok": True, "message": "Task {id} added successfully.".format(id=task["id"])})


@check_right_request_decorator([RIGHTS.EDIT_DB_TASKS])
def admin_edit_task(request):
    body = json.loads(request.body)
    conn = connections["default"]
    cur = conn.cursor()
    cur.execute("""
        UPDATE public.tasks
        SET stage = %s,
         python_exe = %s,
         args = %s,
         is_rerun_on_startup = %s,
         is_resume_on_startup = %s
        WHERE id = %s;
    """, (body["data"]["stage"],
          body["data"]["python_exe"],
          json.dumps(body["data"]["args"]),
          body["data"]["is_rerun_on_startup"],
          body["data"]["is_resume_on_startup"],
          body["data"]["id"]
          )
    )
    task_id = body["data"]["id"]
    task = body["data"]
    if bool(body["data"]["is_launch_now"]):  # запускаем/останавливаем задачу при внесении в неё изменений в зависимости от галочки на форме редактирования
        DbTaskManager.get_instance().start_one_task(task)  # если задача уже работает, она будет перезапущена
    else:
        DbTaskManager.get_instance().stop_one_task(task_id)
    return JsonResponse({"is_ok": True, "message": "Task {id} edited successfully.".format(id=task["id"])})


@check_right_request_decorator([RIGHTS.EDIT_DB_TASKS])
def admin_delete_task(request):
    body = json.loads(request.body)
    DbTaskManager.get_instance().stop_one_task(body["id"])  # сначала останавливаем задачу (там проверят, если она не была запущена)
    conn = connections["default"]
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM public.tasks
        WHERE id = %s;
    """, (body["id"],))
    return JsonResponse({"is_ok": True, "message": "Task {id} deleted successfully.".format(id=body["id"])})


@check_right_request_decorator([RIGHTS.EDIT_DB_TASKS])
def admin_start_one_task(request):
    body = json.loads(request.body)
    DbTaskManager.get_instance().start_one_task(body["data"])
    return JsonResponse({"is_ok": True, "message": "Task {id} started successfully.".format(id=body["data"]["id"])})


@check_right_request_decorator([RIGHTS.EDIT_DB_TASKS])
def admin_stop_one_task(request):
    body = json.loads(request.body)
    DbTaskManager.get_instance().stop_one_task(body["id"])
    return JsonResponse({"is_ok": True, "message": "Task {id} paused/stopped successfully.".format(id=body["id"])})


# ====================================
# Администрирование - ПЕРЕВОДЫ СОВЕТОВ
# ====================================

# читать советы могут все админы
def admin_get_all_tips_translations(request):
    accept_language = request.headers['Accept-Language']
    language_key = get_language_key(accept_language)
    conn = connections["default"]
    cur = conn.cursor()
    cur.execute("""
        SELECT public.get_all_tips_translations(_language_key := %s);
    """, (language_key,))
    tips = list(cur.fetchone()[0])
    return JsonResponse(
        {"tips": tips, "is_test_db": Config.BACKEND_IS_USE_TEST_DB},
        safe=False
    )  # unsafe указывается только для запросов БД на языке SQL


@check_right_request_decorator([RIGHTS.EDIT_LANGUAGES_LIST, RIGHTS.EDIT_TIPS_LIST])
def admin_add_tip(request):
    body = json.loads(request.body)
    conn = connections["default"]
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO public.tips_of_the_day (id, tip_on_languages, page_url)
        VALUES ((SELECT MAX(id) + 1 FROM public.tips_of_the_day), %s, %s)
        RETURNING id;
    """, (json.dumps(body["data"]["tip_on_languages"]), body["data"]["page_url"]))
    tip_id = int(cur.fetchone()[0])
    return JsonResponse({"is_ok": True, "message": "Tip {id} added successfully.".format(id=tip_id)})


@check_right_request_decorator([RIGHTS.EDIT_LANGUAGES_LIST, RIGHTS.EDIT_TIPS_LIST])
def admin_edit_tip(request):
    body = json.loads(request.body)

    user_id = _get_admin_user_id_by_password_internal(request)

    conn = connections["default"]
    cur = conn.cursor()
    cur.execute("""
        WITH log_upd AS (
            UPDATE public.changed_tips
            SET admin_user_id = %(user_id)s,  -- only user last modified by, prev user is rewritten
                read_by_user_ids = '[]'::jsonb  -- nobody read yet
            WHERE tip_id = %(tip_id)s
                AND lang_key IS NULL 
            RETURNING 1
        ), log_ins AS (
            INSERT INTO public.changed_tips (tip_id, lang_key, admin_user_id, read_by_user_ids)
            SELECT %(tip_id)s, NULL, %(user_id)s, '[]'::jsonb
            WHERE NOT EXISTS(SELECT 1 FROM log_upd)
        )
        UPDATE public.tips_of_the_day
        SET tip_on_languages = %(tip_on_languages)s,
            page_url = %(page_url)s 
        WHERE id = %(tip_id)s
    """, {
        "tip_id": body["data"]["id"],
        "adminKey": str(body["adminKey"]),
        "user_id": user_id,
        "page_url": body["data"]["page_url"],
        "tip_on_languages": json.dumps(body["data"]["tip_on_languages"]),
    }
    )
    return JsonResponse({"is_ok": True, "message": "Tip {id} edited successfully.".format(id=body["data"]["id"])})


@check_right_request_decorator([RIGHTS.EDIT_LANGUAGES_LIST, RIGHTS.EDIT_TIPS_LIST])
def admin_delete_tip(request):
    body = json.loads(request.body)
    conn = connections["default"]
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM public.tips_of_the_day
        WHERE id = %s;
    """, (body["id"],))
    return JsonResponse({"is_ok": True, "message": "Tip {id} deleted successfully.".format(id=body["id"])})


# Проверка прав внутри, т.к. заранее неизвестно, какие права проверять (язык может быть разным)
def admin_edit_tip_translation(request):
    body = json.loads(request.body)

    rights = [
        RIGHTS.EDIT_LANGUAGES_LIST,
        RIGHTS.EDIT_TIPS_LIST,
        body["langKey"]
    ]
    rights_error = _check_right_request(request, rights)
    if rights_error is not None:
        return rights_error

    user_id = _get_admin_user_id_by_password_internal(request)

    conn = connections["default"]
    cur = conn.cursor()
    cur.execute("""
        WITH log_upd AS (
            UPDATE public.changed_tips
            SET admin_user_id = %(user_id)s,  -- only user last modified by, prev user is rewritten
                read_by_user_ids = '[]'::jsonb  -- nobody read yet
            WHERE tip_id = %(tip_id)s
                AND lang_key = %(langKey)s
            RETURNING 1
        ), log_ins AS (
            INSERT INTO public.changed_tips (tip_id, lang_key, admin_user_id, read_by_user_ids)
            SELECT %(tip_id)s, %(langKey)s, %(user_id)s, '[]'::jsonb
            WHERE NOT EXISTS(SELECT 1 FROM log_upd)
        )
        UPDATE public.tips_of_the_day
        SET tip_on_languages = tip_on_languages || jsonb_build_object(%(langKey)s, %(translationOnLang)s)  -- update chosen language ONLY
        WHERE id = %(tip_id)s
    """, {
        "tip_id": body["id"],
        "langKey": body["langKey"],
        "user_id": user_id,
        "translationOnLang": body["translationOnLang"],
    })
    return JsonResponse({"is_ok": True, "message": "Tip {id} translation {lang_key} edited successfully.".format(id=body["id"], lang_key=body["langKey"])})


# Проверка прав внутри, т.к. заранее неизвестно, какие права проверять (язык может быть разным)
def admin_get_changed_tips(request):
    body = json.loads(request.body)

    rights = [
        RIGHTS.EDIT_LANGUAGES_LIST,
        RIGHTS.EDIT_TIPS_LIST,
        body["langKey"]
    ]
    rights_error = _check_right_request(request, rights)
    if rights_error is not None:
        return rights_error

    user_id = _get_admin_user_id_by_password_internal(request)

    body = json.loads(request.body)
    conn = connections["default"]
    cur = conn.cursor()
    cur.execute("""
        WITH read_before_edit AS (
          SELECT coalesce(json_agg(t), '[]'::json)
          FROM public.changed_tips t
          WHERE %(user_id)s::text::jsonb NOT IN (SELECT el FROM jsonb_array_elements(t.read_by_user_ids) el)
            AND t.admin_user_id IS DISTINCT FROM %(user_id)s
        ), upd_log AS (
          UPDATE public.changed_tips
          SET read_by_user_ids = read_by_user_ids || jsonb_build_array(%(user_id)s)
          WHERE %(user_id)s::text::jsonb NOT IN (SELECT el FROM jsonb_array_elements(read_by_user_ids) el)
            AND admin_user_id IS DISTINCT FROM %(user_id)s
        )
        SELECT *
        FROM read_before_edit;
    """, {
        "user_id": user_id,
    })
    return JsonResponse({"is_ok": True, "message": "Tip {id} deleted successfully.".format(id=body["id"])})


# ====================================
# Администрирование - УПРАВЛЕНИЕ АДМИН-ПОЛЬЗОВАТЕЛЯМИ
# ====================================

@check_right_request_decorator([])
def admin_get_admin_users(request):
    conn = connections["default"]
    cur = conn.cursor()
    cur.execute("""
        SELECT COALESCE(json_agg(t ORDER BY t.description), '[]')
        FROM public.admin_users t
    """)
    admin_users = list(cur.fetchone()[0])
    return JsonResponse(
        {"admin_users": admin_users, "is_test_db": Config.BACKEND_IS_USE_TEST_DB},
        safe=False
    )  # unsafe указывается только для запросов БД на языке SQL


@check_right_request_decorator([])
def admin_add_admin_user(request):
    body = json.loads(request.body)
    conn = connections["default"]
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO public.admin_users(description, password, rights_list, is_blocked)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
    """, (body["data"]["description"], body["data"]["password"], json.dumps(body["data"]["rights_list"]), body["data"]["is_blocked"]))
    admin_user_id = int(cur.fetchone()[0])
    return JsonResponse({"is_ok": True, "message": "User {id} added successfully.".format(id=admin_user_id)})


@check_right_request_decorator([])
def admin_edit_admin_user(request):
    body = json.loads(request.body)
    conn = connections["default"]
    cur = conn.cursor()
    cur.execute("""
        UPDATE public.admin_users
        SET description = %s,
         password = %s,
         rights_list = %s,
         is_blocked = %s
        WHERE id = %s;
    """, (body["data"]["description"],
          body["data"]["password"],
          json.dumps(body["data"]["rights_list"]),
          body["data"]["is_blocked"],
          body["data"]["id"]
          )
    )
    return JsonResponse({"is_ok": True, "message": "User {id} edited successfully.".format(id=body["data"]["id"])})


@check_right_request_decorator([])
def admin_delete_admin_user(request):
    body = json.loads(request.body)
    conn = connections["default"]
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM public.admin_users
        WHERE id = %s;
    """, (body["id"],))
    return JsonResponse({"is_ok": True, "message": "User {id} deleted successfully.".format(id=body["id"])})


# ====================================
# Администрирование через URL из браузера напрямую
# ====================================

def admin_get_count_1(request):
    conn = connections["default"]
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(1)
        FROM public.list;
    """)
    count = int(cur.fetchone()[0])
    return JsonResponse({
        "message": "Count of records in 'public.list' table with parsing stage 1 passed",
        "count": count
    })


def admin_get_count_2(request):
    conn = connections["default"]
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(1)
        FROM public.list
        WHERE type IS NOT NULL;
    """)
    count = int(cur.fetchone()[0])
    return JsonResponse({
        "message": "Count of records in 'public.list' table with parsing stage 2 passed",
        "count": count
    })


def admin_get_count_3(request):
    conn = connections["default"]
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(1)
        FROM public.list
        WHERE parent_id IS NOT NULL;
    """)
    count = int(cur.fetchone()[0])
    return JsonResponse({
        "message": "Count of records in 'public.list' table with parsing stage 3 passed",
        "count": count
    })


def check(request):
    try:
        conn = connections["default"]
        cur = conn.cursor()
        cur.execute("""
            SELECT 'Db is Online'::text;
        """)
        db_message = str(cur.fetchone()[0])
        all_is_ok = True
    except BaseException as ex:
        db_message = str(ex)
        all_is_ok = False
    return JsonResponse({
        "title": "This is wiki_species_tree_parser API-backend",
        "django_state": "Ok",
        "db_state": db_message,
        "info": "Please read README for more abilities.",
        "all_is_ok": all_is_ok
    })
