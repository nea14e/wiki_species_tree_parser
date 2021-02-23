import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {environment} from '../../../environments/environment';
import {AdminResponse, AdminUser, AdminUserList, DbTask, DbTasksList} from '../models-admin';
import {BaseNetworkAdminService} from '../base-network-admin.service';

@Injectable({
  providedIn: 'root'
})
export class AdminUsersNetworkService extends BaseNetworkAdminService {

  constructor(http: HttpClient) {
    super(http);
  }

  public getAdminUsers(adminKey: string): Observable<AdminUserList> {
    // Запрос возвращает либо AdminUserList, либо AdminResponse.
    // Но во втором случае мы превращаем данные в ошибку, поэтому AdminResponse в ответ никогда не выдаётся.
    return this.pipeAdminQueries(
      this.http.post<AdminUserList | AdminResponse>(environment.BACKEND_API_URL + 'admin_get_admin_users', {adminKey})
    );
  }

  public createAdminUser(task: AdminUser, adminKey: string): Observable<AdminResponse> {
    return this.pipeAdminQueries(
      this.http.post<AdminResponse>(environment.BACKEND_API_URL + 'admin_add_admin_user', {adminKey, data: task})
    );
  }

  public saveAdminUser(task: AdminUser, adminKey: string): Observable<AdminResponse> {
    return this.pipeAdminQueries(
      this.http.post<AdminResponse>(environment.BACKEND_API_URL + 'admin_edit_admin_user', {adminKey, data: task})
    );
  }

  public deleteAdminUser(id: number, adminKey: string): Observable<AdminResponse> {
    return this.pipeAdminQueries(
      this.http.post<AdminResponse>(environment.BACKEND_API_URL + 'admin_delete_admin_user', {adminKey, id})
    );
  }

}
