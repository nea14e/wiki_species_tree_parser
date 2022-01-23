import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {BaseNetworkAdminService} from '../network-admin.service';
import {environment} from '../../../environments/environment';
import {AdminResponse, FillingStatsList, TipForTranslation, TipsTranslationList} from '../../models-admin';
import {RootDataKeeperService} from '../../root-data-keeper.service';

@Injectable({
  providedIn: 'root'
})
export class NetworkFillingStatsService extends BaseNetworkAdminService {

  constructor(protected http: HttpClient,
              public rootData: RootDataKeeperService) {
    super(http, rootData);
  }

  public getFillingStats(groupsCount: number, nestedLevel: number, outerGroupNumber: number, isTestData: boolean): Observable<FillingStatsList> {
    // Запрос возвращает либо TipForTranslation[], либо AdminResponse.
    // Но во втором случае мы превращаем данные в ошибку, поэтому AdminResponse в ответ никогда не выдаётся.
    return this.pipeAdminQueries(
      this.http.post<FillingStatsList | AdminResponse>(environment.BACKEND_API_URL + 'admin_get_filling_stats', {
        groupsCount,
        nestedLevel,
        outerGroupNumber,
        isTestData
        })
    );
  }
}
