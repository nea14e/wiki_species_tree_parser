WITH cte(lang_key, comment, translations) AS (
  VALUES ('ru', 'Русский',
    '{
        "site_title": "Дерево видов",
        "site_description": "Биологическая систематика более чем 100 000 видов животных, растений, бактерий и грибов. Этот сайт - просмотрщик Викивидов/Википедии в виде дерева.",
        "translated_only": "Переведённые названия",
        "latin_only": "Только латынь",
        "both_languages": "Оба языка",
        "rank_word": "Ранг",
        "parent_word": "Родитель",
        "read_on_wiki": "Читать на Википедии",
        "search_in_google": "Искать в Google",
        "copy_link_to_share": "Поделиться с друзьями",
        "link_copied": "Ссылка скопирована. Теперь вы можете вставить её в чат с друзьями. На компьютере используйте в чате Ctrl + V либо правую кнопку мыши.",
        "leaves_count": "Примерное количество видов в этом элементе дерева",
        "expanded_tooltip": "Этот элемент дерева раскрыт. Показаны некоторые его потомки. Нажмите на него, чтобы показать всех его потомков. Повторно нажмите, чтобы свернуть его.",
        "selected_tooltip": "Этот элемент дерева сейчас выбран. Показаны все его потомки. Нажмите на него, чтобы свернуть его.",
        "tip_of_the_day_word": "А знаете ли вы?",
        "show_in_tree": "Показать в дереве",
        "next_fact": "Следующий факт",
        "to_tree_root": "К корню дерева",
        "to_tree": "К дереву",
        "go_back": "Назад",
        "go_forward": "Вперёд",
        "search_word": "Поиск",
        "search_tooltip": "Введите здесь начало названия. Можно использовать Латынь.",
        "search_result_empty": "Извините, ничего не нашлось. Попробуйте сформулировать Ваш запрос по-другому.",
        "bookmarks": "Закладки",
        "add_to_bookmarks": "Добавить в закладки",
        "bookmarks_use_cookies_question": "Мы не храним никаких ваших данных у себя. Поэтому функция \"Закладки\" использует Куки, чтобы хранить список выбранных Вами видов в Вашем браузере. Эти данные не будут видны другим сайтам, но могут быть видны другим пользователям этого компьютера. Вы действительно хотите добавить этот элемент в закладки?",
        "delete_bookmark": "Удалить закладку",
        "delete_bookmark_question": "Удалить выбранную закладку?",
        "authors_word": "Авторы",
        "authors_content": "Сделано коллективом добровольцев, в том числе с использованием рабочего времени и ресурсов, щедро предоставленных <a href=\"https://it-avangard.su/\" target=\"_blank\">ООО \"ИТ-Авангард\"</a>.",
        "network_error": "Проверьте подключение к Интернету или попробуйте позже.",
        "admin_welcome_part_1": "Добро пожаловать, ",
        "admin_welcome_part_2": "Ваши права: ",
        "admin_error_wrong_password": "Неправильный пароль.",
        "admin_error_no_right": "У вас нет этого права.",
        "admin_error_blocked": "Этот пользователь был заблокирован.",
        "admin_error_super_admin_only": "Только суперпользователь имеет это право.",
        "admin_panel": "Панель администрирования",
        "admin_password_placeholder": "Вставьте свой пароль сюда и просто работайте",
        "admin_password_error": "Неверный пароль администратора",
        "admin_logout": "Выйти из администрирования",
        "admin_db_tasks": "Задачи БД",
        "admin_tips_list": "Список фактов",
        "admin_users": "Пользователи-администраторы",
        "admin_translate_from_your_current_language": "Переводить с языка своего интерфейса",
        "admin_translate_from_main_admin_language": "Переводить с основного языка админа",
        "show_details": "Показать подробности",
        "language": "Язык",
        "create": "Добавить новый",
        "edit": "Редактировать",
        "delete": "Удалить",
        "save": "Сохранить",
        "cancel": "Отмена",
        "success": "Успешно выполнено."
      }'::jsonb
  ),
    ('en', 'English',
      '{
        "site_title": "Species tree",
        "site_description": "Biological systematics of more than 100,000 species of animals, plants, bacteria and fungi. This site is the viewer of Wikispecies/Wikipedia via tree.",
        "translated_only": "Translated titles",
        "latin_only": "Latin only",
        "both_languages": "Both languages",
        "rank_word": "Rank",
        "parent_word": "Parent",
        "read_on_wiki": "Read on Wikipedia",
        "search_in_google": "Search with Google",
        "copy_link_to_share": "Share with friends",
        "link_copied": "Link copied. Now you can insert it into the chat with your friends. On a computer, use Ctrl + V in chat or the right mouse button.",
        "leaves_count": "Approximate number of species in this tree element",
        "expanded_tooltip": "This tree element is expanded. Some it''s descendants are shown. Click on it to show all of its descendants. Click again to collapse it.",
        "selected_tooltip": "This tree item is now selected. All it''s descendants are shown. Click on it to collapse it.",
        "tip_of_the_day_word": "Do you know?",
        "show_in_tree": "Show in the Tree",
        "next_fact": "Next fact",
        "to_tree": "To the Tree",
        "go_back": "Back",
        "go_forward": "Forward",
        "to_tree_root": "To the tree root",
        "search_word": "Search",
        "search_tooltip": "Enter here beginning of element''s title. Latin also allowed.",
        "search_result_empty": "Sorry, nothing was found. Try to formulate your request differently.",
        "bookmarks": "Bookmarks",
        "add_to_bookmarks": "Add to bookmarks",
        "bookmarks_use_cookies_question": "We do not store any of your data. Therefore, the \"Bookmarks\" function uses Cookies to store a list of the species you have selected in your browser. This data will not be visible to other sites, but may be visible to other users of this computer. Are you sure you want to bookmark this item?",
        "delete_bookmark": "Remove bookmark",
        "delete_bookmark_question": "Remove selected bookmark?",
        "authors_word": "Authors",
        "authors_content": "Made by team of volunteers from <a href=\"https://it-avangard.su/\" target=\"_blank\">https://it-avangard.su/</a> company.",
        "network_error": "Please check Internet connection or try again later.",
        "admin_welcome_part_1": "Welcome, ",
        "admin_welcome_part_2": "Your rights: ",
        "admin_error_wrong_password": "Wrong password.",
        "admin_error_no_right": "You does not have this right.",
        "admin_error_blocked": "This user has been blocked.",
        "admin_error_super_admin_only": "Only super-admin has this right.",
        "admin_panel": "Admin panel",
        "admin_password_placeholder": "Paste your password here and just do work",
        "admin_password_error": "Wrond admin password",
        "admin_logout": "Logout from admin",
        "admin_db_tasks": "DB tasks",
        "admin_tips_list": "Tips list",
        "admin_users": "Admin users",
        "admin_translate_from_your_current_language": "Translate from your interface''s language",
        "admin_translate_from_main_admin_language": "Translate from ",
        "show_details": "Show details",
        "language": "Language",
        "create": "Create",
        "edit": "Edit",
        "delete": "Delete",
        "save": "Save",
        "cancel": "Cancel",
        "success": "Done successfully."
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