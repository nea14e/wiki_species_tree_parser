import json

from django.db import connections
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from species_tree_backend.http_headers_parser import get_language_key

from config import Config
from config_EXAMPLE import Config as ConfigExample


# ====================================
# Собственно для работы приложения
# ====================================

@csrf_exempt
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


@csrf_exempt
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


@csrf_exempt
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


@csrf_exempt
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


@csrf_exempt
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


@csrf_exempt
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


@csrf_exempt
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
# Администрирование через фронтэнд
# ====================================

# Это декоратор для всех функций, где надо проверять ключ админа в теле запроса
def check_admin_request(func):
    def wrapped(*args, **kw):

        if (ConfigExample.BACKEND_SECRET_KEY == Config.BACKEND_SECRET_KEY):
            return JsonResponse({"is_ok": False, "message": "You forgot to change Config.BACKEND_SECRET_KEY when copied from Config_EXAMPLE!"})
        if (ConfigExample.BACKEND_ADMIN_URL_PREFIX == Config.BACKEND_ADMIN_URL_PREFIX):
            return JsonResponse({"is_ok": False, "message": "You forgot to change Config.BACKEND_ADMIN_URL_PREFIX when copied from Config_EXAMPLE!"})

        request = args[0]
        try:
            body = json.loads(request.body)
            if (str(body["adminKey"]) != Config.BACKEND_ADMIN_URL_PREFIX):
                return JsonResponse({"is_ok": False, "message": "Wrong admin key"})
        except BaseException:
            return JsonResponse(
                {
                    "is_ok": False,
                    "message": "All admin's requests must be of HTTP POST type with 'adminKey' provided in POST's json object."
                }
            )

        return func(*args, **kw)

    return wrapped


@check_admin_request
@csrf_exempt
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


@check_admin_request
@csrf_exempt
def admin_get_tasks(request):
    conn = connections["default"]
    cur = conn.cursor()
    cur.execute("""
        SELECT COALESCE(json_agg(t ORDER BY t.stage, t.is_completed, t.id), '[]')
        FROM (
               SELECT *
               FROM public.tasks
          ) t;
    """)
    db_response = cur.fetchone()[0]
    return JsonResponse(db_response, safe=False)  # unsafe указывается только для запросов БД на языке SQL


@check_admin_request
@csrf_exempt
def admin_add_task(request):
    body = json.loads(request.body)
    conn = connections["default"]
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO public.tasks(stage, args, is_run_on_startup)
        VALUES (%s, %s, %s);
    """, (body["data"]["stage"], json.dumps(body["data"]["args"]), body["data"]["is_run_on_startup"]))
    return JsonResponse({"is_ok": True, "message": "Task added successfully."})


@check_admin_request
@csrf_exempt
def admin_edit_task(request):
    body = json.loads(request.body)
    conn = connections["default"]
    cur = conn.cursor()
    cur.execute("""
        UPDATE public.tasks
        SET stage = %s,
         args = %s,
         is_run_on_startup = %s
        WHERE id = %s;
    """, (body["data"]["stage"], json.dumps(body["data"]["args"]), body["data"]["is_run_on_startup"], body["data"]["id"]))
    return JsonResponse({"is_ok": True, "message": "Task edited successfully."})


@check_admin_request
@csrf_exempt
def admin_delete_task(request):
    body = json.loads(request.body)
    conn = connections["default"]
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM public.tasks
        WHERE id = %s;
    """, (body["id"],))
    return JsonResponse({"is_ok": True, "message": "Task deleted successfully."})


# ====================================
# Администрирование через URL из браузера напрямую
# ====================================

@csrf_exempt
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


@csrf_exempt
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


@csrf_exempt
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


@csrf_exempt
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
