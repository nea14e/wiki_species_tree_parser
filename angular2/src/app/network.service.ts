import {inject, Injectable, Service} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {environment} from '../environments/environment';
import {TranslationRoot} from './models/translation-root';
import {TipOfTheDay} from './models/tip-of-the-day';
import {Tree} from './models/tree';
import {FavoritesItem} from './models/favorites-item';
import {SearchItem} from './models/search-item';

export const NETWORK_ERROR_DEFAULT_MESSAGE = 'Ошибка сети. Проверьте интернет-соединение.';

@Service()
export class NetworkService {

  private _http = inject(HttpClient);

  public getTranslations(): Observable<TranslationRoot> {
    return this._http.get<TranslationRoot>(environment.BACKEND_API_URL + 'get_translations');
  }

  public getTipOfTheDay(): Observable<TipOfTheDay> {
    return this._http.get<TipOfTheDay>(environment.BACKEND_API_URL + 'get_tip_of_the_day');
  }

  public getTipOfTheDayById(id: number): Observable<TipOfTheDay> {
    return this._http.get<TipOfTheDay>(environment.BACKEND_API_URL + 'get_tip_of_the_day_by_id/' + id);
  }

  public getTreeDefault(): Observable<Tree> {
    return this._http.get<Tree>(environment.BACKEND_API_URL + 'get_tree_default');
  }

  public getTreeById(id: number): Observable<Tree> {
    return this._http.get<Tree>(environment.BACKEND_API_URL + 'get_tree_by_id/' + id);
  }

  public getFavorites(ids: number[]): Observable<FavoritesItem[]> {
    return this._http.post<FavoritesItem[]>(environment.BACKEND_API_URL + 'get_favorites', {ids});
  }

  public search(query: string, limit: number, offset: number = 0): Observable<SearchItem[]> {
    return this._http.get<SearchItem[]>(environment.BACKEND_API_URL + 'search_by_words', {
      params: {
        query,
        limit: limit.toString(),
        offset: offset.toString()
      }
    });
  }

}
