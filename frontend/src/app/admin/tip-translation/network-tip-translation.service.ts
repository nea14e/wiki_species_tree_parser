import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {BaseNetworkAdminService} from '../network-admin.service';
import {environment} from '../../../environments/environment';
import {AdminResponse, TipForTranslation, TipsTranslationList} from '../../models-admin';
import {RootDataKeeperService} from '../../root-data-keeper.service';

@Injectable({
  providedIn: 'root'
})
export class NetworkTipTranslationService extends BaseNetworkAdminService {

  constructor(protected http: HttpClient,
              public rootData: RootDataKeeperService) {
    super(http, rootData);
  }

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

  public attachTipToTree(tipId: number, speciesPageUrl: string, adminKey: string): Observable<AdminResponse> {
    return this.pipeAdminQueries(
      this.http.post<AdminResponse>(environment.BACKEND_API_URL + 'admin_attach_tip_to_tree',
        {adminKey, tipId, speciesPageUrl})
    );
  }

  public detachTipFromTree(tipId: number, adminKey: string): Observable<AdminResponse> {
    return this.pipeAdminQueries(
      this.http.post<AdminResponse>(environment.BACKEND_API_URL + 'admin_detach_tip_from_tree', {adminKey, tipId})
    );
  }

  public saveTipTranslation(langKey: string, id: number, translationOnLang: string, adminKey: string): Observable<AdminResponse> {
    return this.pipeAdminQueries(
      this.http.post<AdminResponse>(environment.BACKEND_API_URL + 'admin_edit_tip_translation', {adminKey, id, langKey, translationOnLang})
    );
  }

}
