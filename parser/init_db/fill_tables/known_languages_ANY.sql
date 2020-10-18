WITH cte(lang_key, comment, translations) AS (
  VALUES ('ru', 'Русский',
    '{
        "site_title": "Дерево видов",
        "site_description": "Биологическая систематика более чем 100 000 видов животных, растений, бактерий и грибов. Фотографии и информация для построения дерева взяты из проекта Викивиды",
        "rank_word": "Ранг",
        "parent_word": "Родитель",
        "read_on_wiki": "Читать на Википедии",
        "search_in_google": "Искать в Google",
        "copy_link_to_share": "Поделиться с друзьями",
        "link_copied": "Ссылка скопирована. Теперь вы можете вставить её в чат с друзьями. На компьютере используйте в чате Ctrl + V либо правую кнопку мыши.",
        "tip_of_the_day_word": "А знаете ли вы?",
        "show_in_tree": "Показать в дереве",
        "next_fact": "Следующий факт",
        "to_tree_root": "К корню дерева",
        "search_word": "Поиск",
        "search_result_empty": "Извините, ничего не нашлось. Попробуйте сформулировать Ваш запрос по-другому.",
        "bookmarks": "Закладки",
        "add_to_bookmarks": "Добавить в закладки",
        "bookmarks_use_cookies_question": "Мы не храним никаких ваших данных у себя. Поэтому функция \"Закладки\" использует Куки, чтобы хранить список выбранных Вами видов в Вашем браузере. Эти данные не будут видны другим сайтам, но могут быть видны другим пользователям этого компьютера. Вы действительно хотите добавить этот элемент в закладки?",
        "delete_bookmark": "Удалить закладку",
        "delete_bookmark_question": "Удалить выбранную закладку?",
        "authors_word": "Авторы",
        "authors_content": "Сделано коллективом добровольцев, в том числе с использованием рабочего времени и ресурсов, щедро предоставленных <a href=\"https://it-avangard.su/\">ООО \"ИТ-Авангард\"</a>."
      }'::jsonb
  ),
    ('en', 'English',
      '{
        "site_title": "Species tree",
        "site_description": "Biological systematics of more than 100,000 species of animals, plants, bacteria and fungi. Photos and information for building a tree are taken from the Wikispecies/Wikipedia project",
        "rank_word": "Rank",
        "parent_word": "Parent",
        "read_on_wiki": "Read on Wikipedia",
        "search_in_google": "Search with Google",
        "copy_link_to_share": "Share with friends",
        "link_copied": "Link copied. Now you can insert it into the chat with your friends. On a computer, use Ctrl + V in chat or the right mouse button.",
        "tip_of_the_day_word": "Do you know?",
        "show_in_tree": "Show in the Tree",
        "next_fact": "Next fact",
        "to_tree_root": "To the tree root",
        "search_word": "Search",
        "search_result_empty": "Sorry, nothing was found. Try to formulate your request differently.",
        "bookmarks": "Bookmarks",
        "add_to_bookmarks": "Add to bookmarks",
        "bookmarks_use_cookies_question": "We do not store any of your data. Therefore, the \"Bookmarks\" function uses Cookies to store a list of the species you have selected in your browser. This data will not be visible to other sites, but may be visible to other users of this computer. Are you sure you want to bookmark this item?",
        "delete_bookmark": "Remove bookmark",
        "delete_bookmark_question": "Remove selected bookmark?",
        "authors_word": "Authors",
        "authors_content": "Made by team of volunteers from <a href=\"https://it-avangard.su/\">https://it-avangard.su/</a> company."
      }'::jsonb
    )
),
     upd AS (
       UPDATE public.known_languages
         SET
           comment = cte.comment,
           translations = cte.translations
         FROM cte
         WHERE known_languages.lang_key = cte.lang_key
         RETURNING cte.lang_key
     ),
     ins AS (
       INSERT INTO public.known_languages
         SELECT *
         FROM cte
         WHERE cte.lang_key NOT IN (SELECT lang_key
                                    FROM upd)
         RETURNING lang_key
     )
DELETE
FROM public.known_languages
WHERE lang_key NOT IN (SELECT lang_key
                       FROM upd)
  AND lang_key NOT IN (SELECT lang_key
                       FROM ins);