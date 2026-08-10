import {Right} from './right';

export class AdminUser {
  id!: number;
  description!: string;
  password!: string;
  rights_list: Right[] = [];
  is_blocked = false;
}
