import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {BaseNetworkAdminService} from '../network-admin.service';
import {environment} from '../../../environments/environment';
import {AdminResponse, DbTask, DbTasksList} from '../../models-admin';
import {RootDataKeeperService} from '../../root-data-keeper.service';

@Injectable({
  providedIn: 'root'
})
export class NetworkDbTasksService extends BaseNetworkAdminService {

  constructor(protected http: HttpClient,
              public rootData: RootDataKeeperService) {
    super(http, rootData);
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
