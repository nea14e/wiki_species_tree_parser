import {Level} from './level';
import {SelectedLanguageKey1} from '../common/models/selected-language-key1';
import {SelectedLanguageKey2} from '../common/models/selected-language-key2';

export interface Tree {
  _id: number;
  levels: Level[];
  _language_key1: SelectedLanguageKey1;
  _language_key2: SelectedLanguageKey2;
}
