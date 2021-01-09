class Config:

    # ============== Общее для парсера и бэкенда: =======================

    # Режим отладки
    IS_DEBUG = False

    DB_HOST = str("127.0.0.1")
    # DB_HOST = str("192.168.33.147")
    DB_PORT = str("5432")
    DB_USER = str("postgres")
    DB_PASSWORD = str("12345")

    # ============== Для бэкенда: =======================

    BACKEND_IS_USE_TEST_DB = True  # Использует ли бэкенд тестовую базу данных 'lifetree_test' или основную `lifetree`

    # Придумайте его сами и ДЕРЖИТЕ В СЕКРЕТЕ:
    BACKEND_SECRET_KEY = "3ie74_tbjloei6icg2+_a@g3nd9w+kruw@6turwe34AS9IVGFDOP0324"  # Просто некий ключ для работы бэкенда Django.
    # Придумайте его сами и ДЕРЖИТЕ В СЕКРЕТЕ:
    BACKEND_ADMIN_URL_PREFIX = "asdfGBJ8921sayuwire893uir"  # С этого префикса будут начинаться URL, предназначенные для обслуживания парсера/базы данных. Запросы по этим URL могут надолго повесить базу.

    # ============== Для парсера: =======================

    # Задаёт интервал отдыха между концом парсинга предыдущей страницы и началом загрузки следующей (в секундах).
    # Поскольку парсинг страницы Викивидов и связанных с ней Википедий по языкам занимают значительное время,
    # реальный интервал между загрузкой предыдущей страницы и следующей будет значительно больше этого числа.
    NEXT_PAGE_DELAY = 0.01

    # URL-адреса и маски для них. Иногда надо их править.
    URL_DOMAIN = "https://species.wikimedia.org/"
    URL_START = "https://species.wikimedia.org/wiki/"
    URL_START_RELATIVE = "/wiki/"
    WIKIPEDIAS_URL_MASK = r"https:\/\/(.+)\.wikipedia\.org\/wiki\/(.+)"
    WIKIPEDIA_URL_CONSTRUCTOR = "https://{}.wikipedia.org/wiki/{}"

    PROC_STATE_UPDATE_TIMER = 3.0
    LOGS_UPDATE_TIMER = 3.0
    LOGS_KEEP_LINES_COUNT = 50

    LOGS_ERROR_PREFIX = "$$$"
