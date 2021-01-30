/* tslint:disable:variable-name */
import {Translations} from './models';

export class Right {
  constructor(public r: string) {
  }
}

export const RIGHTS = {
  SUPER_ADMIN: new Right('[SUPER_ADMIN]'),  // фиктивное право, которое есть только у суперадмина и выдать никому его нельзя
  CONTROL_DB_TASKS: new Right('[CONTROL_DB_TASKS]'),
  ADD_EDIT_ANY_LANGUAGES: new Right('[ADD_EDIT_ANY_LANGUAGES]'),
  ADD_EDIT_ANY_TIPS: new Right('[ADD_EDIT_ANY_TIPS]'),
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

export class TipsTranslationList {
  tips: TipForTranslation[] = [];
  is_test_db: boolean;
}

export class TipForTranslation {
  id: number;
  tip_on_languages: TranslationsByLanguages;
  species_id: number;
  page_url: string;
  image_url: string;
  titles_by_languages: TranslationsByLanguages;
  wikipedias_by_languages: TranslationsByLanguages;
  title_by_latin: string;
  title_by_admin: string;
  title_by_language: string;
  rank_by_admin: string;
  rank_by_language: string;
}

export class TranslationsByLanguages {
  [key: string]: string | null;
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

export class AdminLoginInfo {
  description: string;
  rights_list: Right[] = [];
}

export class AdminLanguage {
  lang_key: string;
  comment: string;
  translations: Translations;
}

export class AdminMainLanguage {
  lang_key: string;
  comment: string;
}

export class AdminResponse {
  is_ok: boolean;
  message_translation_key: string | null;
  message: string;
}
