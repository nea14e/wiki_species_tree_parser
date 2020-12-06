CREATE TABLE public.tasks (
  id bigserial NOT NULL,
  stage text NOT NULL,  -- тип задачи (стадия: '0', '1', 'parse_language', ...)
  python_exe text NOT NULL,  -- название запускаемого файла Python 3
  args json NOT NULL DEFAULT '{}',  -- входные аргументы при его запуске (распарсенные по именам в словарь)
  is_run_on_startup bool NOT NULL DEFAULT false,  -- Это поле нужно только, чтобы знать, какие процессы запускать при старте бэкенда.
  is_success bool NULL,  -- завершена ли: TRUE = с успехом или FALSE = без успеха, NULL = ещё не завершена (такие задачи тоже не перезапускаются)
  last_crash_message text,  -- текст последней ошибки (имеются в виду только критические, когда процесс парсера упал)
  CONSTRAINT pk_tasks PRIMARY KEY (id)
)