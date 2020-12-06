/* tslint:disable:variable-name */
import {Translations} from "./models";

export class DbTask {
  id: number | null;
  stage: string;
  python_exe = 'python3';
  args: DbTaskArgs = new DbTaskArgs();
  is_run_on_startup = true;
  is_success = false;
  is_running_now: string;
  recent_logs: string;
}

export class DbTaskArgs {
  is_test = false;
  from_title: string;
  to_title: string;
  skip_parsed_interval = true;
  where: string;
  lang_key: string;
  proxy: string;
}

export class AdminLanguage {
  lang_key: string;
  comment: string;
  translations: Translations;
}

export class AdminResponse {
  is_ok: boolean;
  message: string;
}
