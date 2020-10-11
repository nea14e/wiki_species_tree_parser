export interface Tree {
  _id: number;
  levels: Level[];
  translation: Translation;
  _language_key: string;
}

export interface Translation {
  comment: string;
  lang_key: string;
  rank_word: string;
  site_title: string;
  parent_word: string;
  search_word: string;
  authors_word: string;
  authors_content: string;
  site_description: string;
  tip_of_the_day_word: string;
}

export interface Level {
  type: string;
  items: Item[];
  title_on_language: string;
  level_parent_title: string;
  is_level_has_selected_item: boolean;
}

export interface Item {
  id: number;
  page_url: string;
  image_url: string;
  parent_id?: number;
  is_expanded: boolean;
  is_selected: boolean;
  leaves_count: number;
  title_for_language: string;
  wiki_url_for_language: string;
}
