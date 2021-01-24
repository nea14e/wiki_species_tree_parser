import { Injectable } from '@angular/core';
import {TranslationRoot} from './models';
import {Params} from '@angular/router';
import {AdminLoginInfo, RIGHTS} from './models-admin';

@Injectable({
  providedIn: 'root'
})
export class RootDataKeeperService {

  public adminPassword: string;
  adminLoginInfo: AdminLoginInfo | null;
  public translationRoot: TranslationRoot;
  public lastTipParams: Params;
  public lastTreeParams: Params;
  public lastSearchParams: Params;

  constructor() { }

  checkRight(r: string): boolean {
    return !!this.adminLoginInfo
      && this.adminLoginInfo.rights_list.some(right => right.r === r);
  }

  canDbTasks(): boolean {
    return !!this.adminLoginInfo
      && this.adminLoginInfo.rights_list.some(right => right.r === RIGHTS.SUPER_ADMIN.r || RIGHTS.ALL_EXCEPT_CONTROL_USER.r);
  }

  canSeeTipTranslation(): boolean {
    return !!this.adminLoginInfo;
  }

  canManageAdminUsers(): boolean {
    return !!this.adminLoginInfo
      && this.adminLoginInfo.rights_list.some(right => right.r === RIGHTS.SUPER_ADMIN.r);
  }
}
