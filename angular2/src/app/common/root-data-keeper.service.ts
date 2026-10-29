import {Service, signal} from '@angular/core';
import {Params} from '@angular/router';
import {AdminLoginInfo} from '../admin/models/admin-login-info';
import {AdminMainLanguage} from '../admin/models/admin-main-language';
import {TranslationRoot} from '../models/translation-root';
import {RIGHTS} from '../admin/models/right';
import {Subject} from 'rxjs';
import {SelectedLanguagesInfo} from './models/selected-languages-info';
import {SelectedLanguageKey1} from './models/selected-language-key1';
import {SelectedLanguageKey2} from './models/selected-language-key2';

@Service()
export class RootDataKeeperService {

  public adminPassword: string | null = null;
  public adminLoginInfo: AdminLoginInfo | null = null;
  private _selectedLanguageKey1 = signal<SelectedLanguageKey1>("auto");
  public selectedLanguageKey1 = this._selectedLanguageKey1.asReadonly();
  private _selectedLanguageKey2 = signal<SelectedLanguageKey2>("latin");
  public selectedLanguageKey2 = this._selectedLanguageKey2.asReadonly();
  public languagesChangedSubject = new Subject<SelectedLanguagesInfo>();
  public translationRoot = signal<TranslationRoot | null>(null);
  public isTranslateFromYourLang = false;
  public mainAdminLanguage: AdminMainLanguage | null = null;
  public lastTipId: number | null = null;
  public lastTreeId: number | null = null;
  public lastSearchParams: Params = {};

  selectLanguageKey1(langKey: SelectedLanguageKey1) {
    if (this._selectedLanguageKey1() === langKey) {
      return;
    }
    this._selectedLanguageKey1.set(langKey);
    this.languagesChangedSubject.next({
      selectedLanguageKey1: langKey,
      selectedLanguageKey2: this._selectedLanguageKey2()
    } as SelectedLanguagesInfo);
  }

  selectLanguageKey2(langKey: SelectedLanguageKey2) {
    if (this._selectedLanguageKey2() === langKey) {
      return;
    }
    this._selectedLanguageKey2.set(langKey);
    this.languagesChangedSubject.next({
      selectedLanguageKey1: this._selectedLanguageKey1(),
      selectedLanguageKey2: langKey
    } as SelectedLanguagesInfo);
  }

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
