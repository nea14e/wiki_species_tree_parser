import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {BaseNetworkAdminService} from '../network-admin.service';
import {environment} from '../../../environments/environment';
import {AdminLanguage, AdminResponse, DbTask, DbTasksList} from '../../models-admin';

@Injectable({
  providedIn: 'root'
})
export class NetworkDbTasksService extends BaseNetworkAdminService {

  constructor(private http: HttpClient) {
    super();
  }

  public getDbTasks(adminKey: string): Observable<DbTasksList> {
    // Запрос возвращает либо DbTask[], либо AdminResponse.
    // Но во втором случае мы превращаем данные в ошибку, поэтому AdminResponse в ответ никогда не выдаётся.
    return this.pipeAdminQueries(
      this.http.post<DbTasksList | AdminResponse>(environment.BACKEND_API_URL + 'admin_get_tasks', {adminKey})
    );
  }

  public createTask(task: DbTask, adminKey: string): Observable<AdminResponse> {
    return this.pipeAdminQueries(
      this.http.post<AdminResponse>(environment.BACKEND_API_URL + 'admin_add_task', {adminKey, data: task})
    );
  }

  public saveTask(task: DbTask, adminKey: string): Observable<AdminResponse> {
    return this.pipeAdminQueries(
      this.http.post<AdminResponse>(environment.BACKEND_API_URL + 'admin_edit_task', {adminKey, data: task})
    );
  }

  public deleteTask(id: number, adminKey: string): Observable<AdminResponse> {
    return this.pipeAdminQueries(
      this.http.post<AdminResponse>(environment.BACKEND_API_URL + 'admin_delete_task', {adminKey, id})
    );
  }

  public getKnownLanguagesAll(adminKey: string): Observable<AdminLanguage[]> {
    return this.pipeAdminQueries(
      this.http.post<AdminLanguage[] | AdminResponse>(environment.BACKEND_API_URL + 'admin_get_known_languages_all', {adminKey})
    );
  }

  public startOneTask(task: DbTask, adminKey: string): Observable<AdminResponse> {
    return this.pipeAdminQueries(
      this.http.post<AdminResponse>(environment.BACKEND_API_URL + 'admin_start_one_task', {adminKey, data: task})
    );
  }

  public stopOneTask(id: number, adminKey: string): Observable<AdminResponse> {
    return this.pipeAdminQueries(
      this.http.post<AdminResponse>(environment.BACKEND_API_URL + 'admin_stop_one_task', {adminKey, id})
    );
  }

}
