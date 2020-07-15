def get_language_key(accept_language: str) -> str:
    """
    This function based on one by: Siong-Ui Te
    Got from https://siongui.github.io/2012/10/11/python-parse-accept-language-in-http-request-header/
    :param accept_language: str: значение заголовока "Accept-Language" HTTP-запроса браузера пользователя
    :return: language_key, чтобы соответствовать таблице БД public.known_languages
    """
    # accept_language - например, "en-us; q=0.8, en; q=0.6"
    language = accept_language.split(",")[0]  # Например, "en-us; q=0.8"
    locale = language.split(";")[0].strip()  # Например, "en-us"
    lang_key = locale.split("-")[0].strip()  # Например, "en"
    return lang_key
