import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {Observable} from 'rxjs';
import {TranslationRoot, Tree} from './models';
import {environment} from '../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class NetworkService {

  constructor(private http: HttpClient) { }

  public getTranslations(): Observable<TranslationRoot> {
    return this.http.get<TranslationRoot>(environment.BACKEND_API_URL + 'get_translations');
  }

  public getTreeDefault(): Observable<Tree> {
    return this.http.get<Tree>(environment.BACKEND_API_URL + 'get_tree_default');
  }

  public getTreeById(id: number): Observable<Tree> {
    return this.http.get<Tree>(environment.BACKEND_API_URL + 'get_tree_by_id/' + id);
  }

}
