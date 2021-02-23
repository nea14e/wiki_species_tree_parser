import {HttpClient} from '@angular/common/http';
import {Observable, of, throwError} from 'rxjs';
import {AdminLanguage, AdminResponse} from './models-admin';
import {environment} from '../../environments/environment';
import {catchError, switchMap} from 'rxjs/operators';

export class BaseNetworkAdminService {
  constructor(protected http: HttpClient) {
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
          return throwError(null);
        }),
        switchMap(response => {
          if ('is_ok' in response) {
            if (response.is_ok === false) {
              return throwError(response.message);  // Послать дальше по трубе ошибку
            }
          }
          return of(response as T);  // Послать дальше по трубе данные
          // Так как throwError() возвращает Observable, то используется метод switchMap(), возвращающий Observable,
          // и здесь нам тоже надо из данных сконструировать новый Observable с помощью of().
        })
      );
  }
}
