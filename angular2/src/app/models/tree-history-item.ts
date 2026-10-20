import {Item} from './item';
import {v4} from 'uuid';

export class TreeHistoryItem {
  item: Item | null;
  random_id: string;

  constructor(item: Item | null) {
    this.item = item;
    this.random_id = v4();
  }
}
