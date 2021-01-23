/* tslint:disable:variable-name */
import {Translations} from './models';

export class Right {
  constructor(public r: string) {
  }
}

export const RIGHTS = {
  ALL_EXCEPT_CONTROL_USER: new Right('[All except control users]'),
  ADD_EDIT_ANY_LANGUAGES: new Right('[Add/edit any languages, translations]'),
};

export class DbTasksList {
  tasks: DbTask[] = [];
  is_test_db: boolean;
}

export class DbTask {
  id: number | null;
  stage: string;
  python_exe = 'python3';
  args: DbTaskArgs = new DbTaskArgs();
  is_rerun_on_startup: boolean;
  is_resume_on_startup: boolean;
  is_launch_now = true;
  is_success = false;
  is_running_now: boolean;
  recent_stdout: string;
  recent_stderr: string;
}

export class DbTaskArgs {
  from_title: string;
  to_title: string;
  skip_parsed_interval = true;
  where: string;
  lang_key: string;
  proxy: string;
  timeout = 35;
  will_success = true;
}

export class AdminUsersList {
  admin_users: AdminUser[] = [];
  is_test_db: boolean;
}

export class AdminUser {
  id: number;
  description: string;
  password: string;
  rights_list: Right[] = [];
  is_blocked = false;
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
