import {Translations} from '../../models/translations';

export class AdminResponse {
  is_ok!: boolean;
  message_translation_key!: keyof Translations;
  message!: string;
}
