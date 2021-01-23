import {Observable, of, throwError} from 'rxjs';
import {AdminLanguage, AdminResponse, AdminLoginInfo} from '../models-admin';
import {catchError, switchMap} from 'rxjs/operators';
import {HttpClient} from '@angular/common/http';
import {environment} from '../../environments/environment';
import {RootDataKeeperService} from '../root-data-keeper.service';
import {Injectable} from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class BaseNetworkAdminService {

  constructor(protected http: HttpClient,
              public rootData: RootDataKeeperService) {
  }

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

  /*
      Оборачиваем все Observable сетевых запросов админки в этот метод.
      Все запросы админки могут вместо данных положенного типа T вернуть AdminResponse с ошибкой.
      Здесь мы выделяем этот AdminResponse и в этом случае кидаем дальше по трубе ошибку,
      чтобы в Subscribe() вызвался error вместо next для отображения ошибки, а next был бы рассчитан только на основной тип данных.
     */
  protected pipeAdminQueries<T>(obs: Observable<T | AdminResponse>): Observable<T> {
    return obs
      .pipe(
        catchError(() => {
          // Заменяем все ошибки запросов (где в ответ не пришли данные с текстом ошибки) на null,
          // чтобы в Observable() снаружи можно было отличить эти два случая ошибок
          const translatedMessage = this.rootData.translationRoot?.translations.network_error;
          const defaultMessage = 'Network error. Try again later.';
          return throwError(translatedMessage || defaultMessage);
        }),
        switchMap(response => {
          if ('is_ok' in response) {
            if (response.is_ok === false) {
              if (!!response.message_translation_key) {
                return throwError(this.rootData.translationRoot?.translations[response.message_translation_key]);
              } else {
                return throwError(response.message);  // Послать дальше по трубе ошибку
              }
            }
          }
          return of(response as T);  // Послать дальше по трубе данные
          // Так как throwError() возвращает Observable, то используется метод switchMap(), возвращающий Observable,
          // и здесь нам тоже надо из данных сконструировать новый Observable с помощью of().
        })
      );
  }
}
