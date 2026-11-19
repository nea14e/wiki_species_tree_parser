import {Injectable} from '@angular/core';
import {Observable} from 'rxjs';
import {BaseNetworkAdminService} from '../network-admin.service';
import {environment} from '../../../environments/environment';
import {TipsTranslationList} from '../models/tips-translation-list';
import {AdminResponse} from '../models/admin-response';
import {TipForTranslation} from '../models/tip-for-translation';

@Injectable({
  providedIn: 'root'
})
export class NetworkTipTranslationService extends BaseNetworkAdminService {

  public getTipsTranslations(adminKey: string): Observable<TipsTranslationList> {
    // Запрос возвращает либо TipForTranslation[], либо AdminResponse.
    // Но во втором случае мы превращаем данные в ошибку, поэтому AdminResponse в ответ никогда не выдаётся.
    return this.pipeAdminQueries(
      this.http.post<TipsTranslationList | AdminResponse>(environment.BACKEND_API_URL + 'admin_get_all_tips_translations', {adminKey})
    );
  }

  public createTip(tip: TipForTranslation, langKey: string, adminKey: string): Observable<AdminResponse> {
    return this.pipeAdminQueries(
      this.http.post<AdminResponse>(environment.BACKEND_API_URL + 'admin_add_tip', {adminKey, langKey, data: tip})
    );
  }

  public saveTip(tip: TipForTranslation, langKey: string, adminKey: string): Observable<AdminResponse> {
    return this.pipeAdminQueries(
      this.http.post<AdminResponse>(environment.BACKEND_API_URL + 'admin_edit_tip', {adminKey, langKey, data: tip})
    );
  }

  public deleteTip(id: number, adminKey: string): Observable<AdminResponse> {
    return this.pipeAdminQueries(
      this.http.post<AdminResponse>(environment.BACKEND_API_URL + 'admin_delete_tip', {adminKey, id})
    );
  }

  public attachTipToTree(tipId: number, speciesId: number, adminKey: string): Observable<AdminResponse> {
    return this.pipeAdminQueries(
      this.http.post<AdminResponse>(environment.BACKEND_API_URL + 'admin_attach_tip_to_tree',
        {adminKey, tipId, speciesId})
    );
  }

  public detachTipFromTree(tipId: number, adminKey: string): Observable<AdminResponse> {
    return this.pipeAdminQueries(
      this.http.post<AdminResponse>(environment.BACKEND_API_URL + 'admin_detach_tip_from_tree', {adminKey, tipId})
    );
  }

  public saveTipTranslation(langKey: string, id: number, translationOnLang: string, adminKey: string): Observable<AdminResponse> {
    return this.pipeAdminQueries(
      this.http.post<AdminResponse>(environment.BACKEND_API_URL + 'admin_edit_tip_translation', {
        adminKey,
        id,
        langKey,
        translationOnLang
      })
    );
  }

}
