import {Injectable} from '@angular/core';
import {Observable} from 'rxjs';
import {BaseNetworkAdminService} from '../network-admin.service';
import {environment} from '../../../environments/environment';
import {FillingStatsList} from '../models/filling-stats-list';
import {AdminResponse} from '../models/admin-response';

@Injectable({
  providedIn: 'root'
})
export class NetworkFillingStatsService extends BaseNetworkAdminService {

  getFillingStats(pageUrlFrom: string | null,
                  pageUrlTo: string | null,
                  groupsCount: number,
                  languageKey: string | null,
                  isTestData: boolean): Observable<FillingStatsList> {
    // Запрос возвращает либо FillingStatsList, либо AdminResponse.
    // Но во втором случае мы превращаем данные в ошибку, поэтому AdminResponse в ответ никогда не выдаётся.
    return this.pipeAdminQueries(
      this.http.post<FillingStatsList | AdminResponse>(environment.BACKEND_API_URL + 'admin_get_filling_stats', {
        pageUrlFrom,
        pageUrlTo,
        groupsCount,
        languageKey,
        isTestData
      })
    );
  }
}
