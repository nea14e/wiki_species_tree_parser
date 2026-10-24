import {Item} from './item';
import {v4} from 'uuid';
import {Level} from './level';

export class TreeHistoryItem {
  level: Level | null;
  item: Item | null;
  random_id: string;

  constructor(level: Level | null, item: Item | null) {
    this.level = level;
    this.item = item;
    this.random_id = v4();
  }
}
