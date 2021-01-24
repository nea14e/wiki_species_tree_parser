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

  public createTip(tip: TipForTranslation, adminKey: string): Observable<AdminResponse> {
    return this.pipeAdminQueries(
      this.http.post<AdminResponse>(environment.BACKEND_API_URL + 'admin_add_task', {adminKey, data: tip})
    );
  }

  public saveTip(tip: TipForTranslation, adminKey: string): Observable<AdminResponse> {
    return this.pipeAdminQueries(
      this.http.post<AdminResponse>(environment.BACKEND_API_URL + 'admin_edit_task', {adminKey, data: tip})
    );
  }

  public deleteTip(id: number, adminKey: string): Observable<AdminResponse> {
    return this.pipeAdminQueries(
      this.http.post<AdminResponse>(environment.BACKEND_API_URL + 'admin_delete_task', {adminKey, id})
    );
  }

}
