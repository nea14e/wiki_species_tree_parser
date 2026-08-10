import {FillingStatsItem} from './filling-stats-item';

export class FillingStatsList {
  stats: FillingStatsItem[] = [];
  language_key!: string;
  is_test_db!: boolean;
}
