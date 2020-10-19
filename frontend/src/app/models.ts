export interface Tree {
  _id: number;
  levels: Level[];
  _language_key: string;
}

export interface TranslationRoot {
  lang_key: string;
  comment: string;
  translations: Translations;
}

export interface Translations {
  bookmarks: string;
  next_fact: string;
  rank_word: string;
  site_title: string;
  translated_only: string;
  latin_only: string;
  both_languages: string;
  link_copied: string;
  parent_word: string;
  search_word: string;
  authors_word: string;
  read_on_wiki: string;
  show_in_tree: string;
  to_tree_root: string;
  authors_content: string;
  delete_bookmark: string;
  add_to_bookmarks: string;
  search_in_google: string;
  site_description: string;
  copy_link_to_share: string;
  search_result_empty: string;
  leaves_count: string;
  expanded_tooltip: string;
  selected_tooltip: string;
  tip_of_the_day_word: string;
  delete_bookmark_question: string;
  bookmarks_use_cookies_question: string;
  go_back: string;
}

export interface TipOfTheDay {
  id: number;
  tip_text: string;
  species_id: number;
  image_url: string;
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
  title_latin: string;
  title_for_language: string;
  wiki_url_for_language: string;
}

export enum LatinModeEnum {
  TranslatedOnly,
  BothLanguages,
  LatinOnly
}
