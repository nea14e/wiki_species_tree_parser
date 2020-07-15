from django.db import connections
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


@csrf_exempt
def get_tree_default(request):
    # TODO accept_language = request.headers['Accept-Language']
    conn = connections["default"]
    sql = """
        SELECT public.get_tree_default();
    """
    cur = conn.cursor()
    cur.execute(sql)
    db_response = str(cur.fetchone()[0])
    return JsonResponse(db_response, safe=False)

# TODO get_tree_by_id

# TODO search_by_text


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
