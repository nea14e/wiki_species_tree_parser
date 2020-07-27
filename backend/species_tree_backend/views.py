from django.db import connections
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from species_tree_backend.http_headers_parser import get_language_key


@csrf_exempt
def get_childes_by_id(request, _id: int):  # выдаёт дочернюю часть дерева для записи с нужным id (все его прямые потомки на разных уровнях)
    accept_language = request.headers['Accept-Language']
    language_key = get_language_key(accept_language)
    conn = connections["default"]
    cur = conn.cursor()
    cur.execute("""
        SELECT public.get_childes_by_id(_id := %s, _language_key := %s);
    """, (_id, language_key,))
    db_response = str(cur.fetchone()[0])
    return JsonResponse(db_response, safe=False)


@csrf_exempt
def get_tree_by_id(request, _id: int):  # выдаёт дерево, раскрытое на записи с нужным id (уровни до него и все его прямые потомки на разных уровнях)
    accept_language = request.headers['Accept-Language']
    language_key = get_language_key(accept_language)
    conn = connections["default"]
    cur = conn.cursor()
    cur.execute("""
        SELECT public.get_tree_by_id(_id := %s, _language_key := %s);
    """, (_id, language_key,))
    db_response = str(cur.fetchone()[0])
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
    db_response = str(cur.fetchone()[0])
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
    db_response = str(cur.fetchone()[0])
    return JsonResponse(db_response, safe=False)


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
    except BaseException as ex:
        db_message = str(ex)
    return JsonResponse({
        "title": "This is wiki_species_tree_parser API-backend",
        "django_state": "Ok",
        "db_state": db_message,
        "info": "Please read README for more abilities."
    })
