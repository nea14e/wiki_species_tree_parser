import {Item} from './item';

export interface Level {
  type: string;
  items: Item[];
  rank_for_language1: string;
  rank_latin: string;
  level_parent_title: string;
  is_level_has_selected_item: boolean;
}
