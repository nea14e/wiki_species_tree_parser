import {Translations} from './translations';

export interface TranslationRoot {
  lang_key: string;
  comment: string;
  translations: Translations;
}
