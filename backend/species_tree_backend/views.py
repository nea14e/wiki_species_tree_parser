from django.db import connections
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from species_tree_backend.http_headers_parser import get_language_key


@csrf_exempt
def get_tree_by_id(request, _id: int):
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
def get_tree_default(request):
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
def search_by_words(request, words: str):
    accept_language = request.headers['Accept-Language']
    language_key = get_language_key(accept_language)
    conn = connections["default"]
    cur = conn.cursor()
    cur.execute("""
        SELECT public.search_by_words(_query := %s, _language_key := %s);
    """, (words, language_key,))
    db_response = str(cur.fetchone()[0])
    return JsonResponse(db_response, safe=False)



@csrf_exempt
def admin_get_count(request):
    conn = connections["default"]
    sql = """
        SELECT COUNT(1)
        FROM public.list;
    """
    cur = conn.cursor()
    cur.execute(sql)
    count = int(cur.fetchone()[0])
    return JsonResponse({
        "message": "Count of records in 'public.list' table",
        "count": count
    })


# TODO ? Some other admin functions


@csrf_exempt
def check(request):
    try:
        conn = connections["default"]
        sql = """
            SELECT 'Db is Ok'::text;
        """
        cur = conn.cursor()
        cur.execute(sql)
        db_message = str(cur.fetchone()[0])
    except BaseException as ex:
        db_message = str(ex)
    return JsonResponse({
        "title": "This is wiki_species_tree_parser API-backend",
        "django_state": "Ok",
        "db_state": db_message,
        "info": "Please read README for more abilities."
    })
