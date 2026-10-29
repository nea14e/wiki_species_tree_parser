import {inject, Service} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {environment} from '../environments/environment';
import {TranslationRoot} from './models/translation-root';
import {TipOfTheDay} from './models/tip-of-the-day';
import {Tree} from './models/tree';
import {SearchItem} from './models/search-item';
import {LanguageListItem} from './models/language-list-item';
import {SelectedLanguageKey1} from './common/models/selected-language-key1';

export const NETWORK_ERROR_DEFAULT_MESSAGE = 'Ошибка сети. Проверьте интернет-соединение.';

@Service()
export class NetworkService {

  private _http = inject(HttpClient);

  public getLanguagesList(): Observable<LanguageListItem[]> {
    return this._http.get<LanguageListItem[]>(environment.BACKEND_API_URL + 'get_languages_list');
  }

  public getTranslations(lang_key: SelectedLanguageKey1): Observable<TranslationRoot> {
    return this._http.get<TranslationRoot>(environment.BACKEND_API_URL + 'get_translations/' + lang_key);
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
