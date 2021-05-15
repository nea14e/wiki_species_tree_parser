import { Injectable } from '@angular/core';
import {TranslationRoot} from './models';
import {Params} from '@angular/router';
import {AdminLoginInfo, AdminMainLanguage, RIGHTS} from './models-admin';

@Injectable({
  providedIn: 'root'
})
export class RootDataKeeperService {

  public adminPassword: string;
  public adminLoginInfo: AdminLoginInfo | null;
  public translationRoot: TranslationRoot;
  public isTranslateFromYourLang = false;
  public mainAdminLanguage: AdminMainLanguage | null = null;
  public lastTipParams: Params;
  public lastTreeParams: Params;
  public lastSearchParams: Params;

  constructor() { }

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

  canTranslateLanguage(langKey: string): boolean {
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
