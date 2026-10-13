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

    BACKEND_IS_USE_TEST_DB = True  # Использует ли бэкенд тестовую базу данных или основную
    TEST_DB_NAME = str("lifetree_test")
    PROD_DB_NAME = str("lifetree")

    # Придумайте его сами и ДЕРЖИТЕ В СЕКРЕТЕ:
    BACKEND_SECRET_KEY = "3ie74_tbjloei6icg2+_a@g3nd9w+kruw@6turwe34AS9IVGFDOP0324"  # Просто некий ключ для работы бэкенда Django.
    # Придумайте его сами и ДЕРЖИТЕ В СЕКРЕТЕ:
    BACKEND_ADMIN_PASSWORD = "asdfGBJ8921sayuwire893uir"  # С этого префикса будут начинаться URL, предназначенные для обслуживания парсера/базы данных. Запросы по этим URL могут надолго повесить базу.

    # ============== Для парсера: =======================

    # Задаёт интервал отдыха между концом парсинга предыдущей страницы и началом загрузки следующей (в секундах).
    # Поскольку парсинг страницы Викивидов и связанных с ней Википедий по языкам занимают значительное время,
    # реальный интервал между загрузкой предыдущей страницы и следующей будет значительно больше этого числа.
    NEXT_LIST_PAGE_DELAY = 8.0  # Для составления списка
    NEXT_DETAILS_PAGE_DELAY = 8.0  # Для детализации
    TOO_MANY_REQUESTS_ADDITIONAL_DELAY = 10.0  # Дополнительное ожидание, когда запросы шлём слишком часто

    # URL-адреса и маски для них. Иногда надо их править.
    API_URL = "https://ru.wikipedia.org/w/api.php"  # "https://ru.ruwiki.ru/w/api.php"
    WIKIPEDIAS_URL_MASK = "https://{}.wikipedia.org/wiki/{}"
    # Создать бота и его пароль можно здесь: https://ru.ruwiki.ru/wiki/Служебная:BotPasswords
    WIKI_USER_NAME = "SpeciesTreeParser@SpeciesTreeParser"
    WIKI_USER_PASSWORD = ""
    WIKI_USER_AGENT = "SpeciesTreeParser/0.1 (https://gitverse.ru/nea14e/wiki_species_tree_parser; enozdrev@yandex.ru)"

    PROC_STATE_UPDATE_TIMER = 3.0
    LOGS_UPDATE_TIMER = 3.0
    LOGS_KEEP_LINES_COUNT = 50

    PARSER_ARGS_DELIMITER = "$$$"
    LOGS_ERROR_PREFIX = "$$$ "
