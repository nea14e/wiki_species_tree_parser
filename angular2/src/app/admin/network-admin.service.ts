import {Observable, of, throwError} from 'rxjs';
import {catchError, switchMap} from 'rxjs/operators';
import {HttpClient} from '@angular/common/http';
import {environment} from '../../environments/environment';
import {RootDataKeeperService} from '../common/root-data-keeper.service';
import {inject, Service} from '@angular/core';
import {AdminLoginInfo} from './models/admin-login-info';
import {AdminResponse} from './models/admin-response';
import {AdminLanguage} from './models/admin-language';
import {AdminMainLanguage} from './models/admin-main-language';
import {NETWORK_ERROR_DEFAULT_MESSAGE} from '../network.service';

@Service()
export class BaseNetworkAdminService {

  protected http = inject(HttpClient);
  public rootData = inject(RootDataKeeperService);

  public tryLogin(adminKey: string): Observable<AdminLoginInfo> {
    return this.pipeAdminQueries(
      this.http.post<AdminLoginInfo | AdminResponse>(environment.BACKEND_API_URL + 'admin_try_login', {adminKey})
    );
  }

  public getKnownLanguagesAll(adminKey: string): Observable<AdminLanguage[]> {
    return this.pipeAdminQueries(
      this.http.post<AdminLanguage[] | AdminResponse>(environment.BACKEND_API_URL + 'admin_get_known_languages_all', {adminKey})
    );
  }

  public getMainAdminLanguage(adminKey: string): Observable<AdminMainLanguage> {
    return this.pipeAdminQueries(
      this.http.post<AdminMainLanguage | AdminResponse>(environment.BACKEND_API_URL + 'admin_get_main_admin_language', {adminKey})
    );
  }

  /*
      Оборачиваем все Observable сетевых запросов админки в этот метод.
      Все запросы админки могут вместо данных положенного типа T вернуть AdminResponse с ошибкой.
      Здесь мы выделяем этот AdminResponse и в этом случае кидаем дальше по трубе ошибку,
      чтобы в Subscribe() вызвался error вместо next для отображения ошибки, а next был бы рассчитан только на основной тип данных.
     */
  protected pipeAdminQueries<T extends object>(obs: Observable<T | AdminResponse>): Observable<T> {
    return obs
      .pipe(
        catchError(() => {
          const translatedMessage = this.rootData.translationRoot()?.translations.network_error;
          return throwError(() => translatedMessage || NETWORK_ERROR_DEFAULT_MESSAGE);
        }),
        switchMap(response => {
          if (response instanceof AdminResponse) {
            if (response.is_ok === false) {
              if (!!response.message_translation_key) {
                return throwError(() => this.rootData.translationRoot()?.translations[response.message_translation_key]);
              } else {
                return throwError(() => response.message);  // Послать дальше по трубе ошибку
              }
            }
          }
          return of(response as T);  // Послать дальше по трубе данные
          // Так как throwError() возвращает Observable, то используется метод switchMap(), возвращающий Observable.
          // Поэтому здесь мы тоже должны вернуть Observable.
        })
      );
  }
}
