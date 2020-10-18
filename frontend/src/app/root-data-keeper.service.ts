import { Injectable } from '@angular/core';
import {TranslationRoot} from './models';

@Injectable({
  providedIn: 'root'
})
export class RootDataKeeperService {

  public translationRoot: TranslationRoot;

  constructor() { }
}
