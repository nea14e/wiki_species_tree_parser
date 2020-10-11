import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {Observable} from 'rxjs';
import {Tree} from './models';

@Injectable({
  providedIn: 'root'
})
export class NetworkService {

  private BACKEND_API_URL = 'http://127.0.0.1:8000/api/';

  constructor(private http: HttpClient) { }

  public getTreeDefault(): Observable<Tree> {
    return this.http.get<Tree>(this.BACKEND_API_URL + 'get_tree_default');
  }

}
