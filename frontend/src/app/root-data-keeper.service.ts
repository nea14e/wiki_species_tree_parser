import { Injectable } from '@angular/core';
import {TranslationRoot} from './models';
import {Params} from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class RootDataKeeperService {

  public adminPassword: string;
  public translationRoot: TranslationRoot;
  public lastTipParams: Params;
  public lastTreeParams: Params;
  public lastSearchParams: Params;

  constructor() { }
}
