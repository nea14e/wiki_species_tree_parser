import {Service, signal} from '@angular/core';
import {Params} from '@angular/router';
import {AdminLoginInfo} from '../admin/models/admin-login-info';
import {AdminMainLanguage} from '../admin/models/admin-main-language';
import {TranslationRoot} from '../models/translation-root';
import {RIGHTS} from '../admin/models/right';

@Service()
export class RootDataKeeperService {

  public adminPassword: string | null = null;
  public adminLoginInfo: AdminLoginInfo | null = null;
  public translationRoot = signal<TranslationRoot | null>(null);
  public isTranslateFromYourLang = false;
  public mainAdminLanguage: AdminMainLanguage | null = null;
  public lastTipParams: Params = {};
  public lastTreeParams: Params = {};
  public lastSearchParams: Params = {};

  checkRight(r: string): boolean {
    return !!this.adminLoginInfo
      && this.adminLoginInfo.rights_list.some(right =>
        right.r === RIGHTS.SUPER_ADMIN.r
        || right.r === r
      );
  }

  canManageDbTasks(): boolean {
    return !!this.adminLoginInfo
      && this.adminLoginInfo.rights_list.some(right =>
        right.r === RIGHTS.SUPER_ADMIN.r
        || right.r === RIGHTS.EDIT_DB_TASKS.r
      );
  }

  canManageLanguages(): boolean {
    return !!this.adminLoginInfo
      && this.adminLoginInfo.rights_list.some(right =>
        right.r === RIGHTS.SUPER_ADMIN.r
        || right.r === RIGHTS.EDIT_LANGUAGES_LIST.r
      );
  }

  canManageTips(): boolean {
    return !!this.adminLoginInfo
      && this.adminLoginInfo.rights_list.some(right =>
        right.r === RIGHTS.SUPER_ADMIN.r
        || right.r === RIGHTS.EDIT_TIPS_LIST.r
      );
  }

  canTranslateTipToLanguage(langKey: string): boolean {
    return !!this.adminLoginInfo
      && this.adminLoginInfo.rights_list.some(right =>
        right.r === RIGHTS.SUPER_ADMIN.r
        || right.r === RIGHTS.EDIT_TIPS_LIST.r
        || right.r === langKey
      );
  }

  canSeeTipTranslation(): boolean {
    return !!this.adminLoginInfo
      && this.adminLoginInfo.rights_list.some(right =>
        right.r !== RIGHTS.EDIT_LANGUAGES_LIST.r
      );
  }

  canManageAdminUsers(): boolean {
    return !!this.adminLoginInfo
      && this.adminLoginInfo.rights_list.some(right =>
        right.r === RIGHTS.SUPER_ADMIN.r
      );
  }
}
