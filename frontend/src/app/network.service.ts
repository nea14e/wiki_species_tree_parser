import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {FavoritesItem, SearchItem, TipOfTheDay, TranslationRoot, Tree} from './models';
import {environment} from '../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class NetworkService {

  constructor(private http: HttpClient) {
  }

  public getTranslations(): Observable<TranslationRoot> {
    return this.http.get<TranslationRoot>(environment.BACKEND_API_URL + 'get_translations');
  }

  public getTipOfTheDay(): Observable<TipOfTheDay> {
    return this.http.get<TipOfTheDay>(environment.BACKEND_API_URL + 'get_tip_of_the_day');
  }

  public getTipOfTheDayById(id: number): Observable<TipOfTheDay> {
    return this.http.get<TipOfTheDay>(environment.BACKEND_API_URL + 'get_tip_of_the_day_by_id/' + id);
  }

  public getTreeDefault(): Observable<Tree> {
    return this.http.get<Tree>(environment.BACKEND_API_URL + 'get_tree_default');
  }

  public getTreeById(id: number): Observable<Tree> {
    return this.http.get<Tree>(environment.BACKEND_API_URL + 'get_tree_by_id/' + id);
  }

  public getFavorites(ids: number[]): Observable<FavoritesItem[]> {
    return this.http.post<FavoritesItem[]>(environment.BACKEND_API_URL + 'get_favorites', {ids});
  }

  public search(query: string, limit: number, offset: number = 0): Observable<SearchItem[]> {
    return this.http.get<SearchItem[]>(environment.BACKEND_API_URL + 'search_by_words', {
      params: {
        query,
        limit: limit.toString(),
        offset: offset.toString()
      }
    });
  }

}
