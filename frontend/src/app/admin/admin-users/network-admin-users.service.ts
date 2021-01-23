import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {BaseNetworkAdminService} from '../network-admin.service';
import {environment} from '../../../environments/environment';
import {AdminLanguage, AdminResponse, AdminUser, AdminUsersList, DbTask, DbTasksList} from '../../models-admin';

@Injectable({
  providedIn: 'root'
})
export class NetworkAdminUsersService extends BaseNetworkAdminService {

  constructor(private http: HttpClient) {
    super();
  }

  public getAdminUsers(adminKey: string): Observable<AdminUsersList> {
    // Запрос возвращает либо DbTask[], либо AdminResponse.
    // Но во втором случае мы превращаем данные в ошибку, поэтому AdminResponse в ответ никогда не выдаётся.
    return this.pipeAdminQueries(
      this.http.post<AdminUsersList | AdminResponse>(environment.BACKEND_API_URL + 'admin_get_admin_users', {adminKey})
    );
  }

  public createAdminUser(user: AdminUser, adminKey: string): Observable<AdminResponse> {
    return this.pipeAdminQueries(
      this.http.post<AdminResponse>(environment.BACKEND_API_URL + 'admin_add_admin_user', {adminKey, data: user})
    );
  }

  public saveAdminUser(user: AdminUser, adminKey: string): Observable<AdminResponse> {
    return this.pipeAdminQueries(
      this.http.post<AdminResponse>(environment.BACKEND_API_URL + 'admin_edit_admin_user', {adminKey, data: user})
    );
  }

  public deleteAdminUser(id: number, adminKey: string): Observable<AdminResponse> {
    return this.pipeAdminQueries(
      this.http.post<AdminResponse>(environment.BACKEND_API_URL + 'admin_delete_admin_user', {adminKey, id})
    );
  }

  public getKnownLanguagesAll(adminKey: string): Observable<AdminLanguage[]> {
    return this.pipeAdminQueries(
      this.http.post<AdminLanguage[] | AdminResponse>(environment.BACKEND_API_URL + 'admin_get_known_languages_all', {adminKey})
    );
  }

}
