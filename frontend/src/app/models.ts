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
  favorites: string;
  next_fact: string;
  rank_word: string;
  site_title: string;
  translated_only: string;
  latin_only: string;
  both_languages: string;
  link_copied: string;
  parent_word: string;
  search_word: string;
  search_tooltip: string;
  authors_word: string;
  read_on_wiki: string;
  show_in_tree: string;
  to_tree_root: string;
  to_tree: string;
  go_back: string;
  go_forward: string;
  authors_content: string;
  delete_favorite: string;
  add_to_favorites: string;
  search_in_google: string;
  site_description: string;
  copy_link_to_share: string;
  search_result_empty: string;
  load_more: string;
  leaves_count: string;
  expanded_tooltip: string;
  selected_tooltip: string;
  tip_of_the_day_word: string;
  delete_favorite_question: string;
  favorites_use_cookies_question: string;
  network_error: string;
  // Admin:
  admin_welcome_part_1: string;
  admin_welcome_part_2: string;
  admin_error_wrong_password: string;
  admin_error_no_right: string;
  admin_error_blocked: string;
  admin_error_super_admin_only: string;
  admin_panel: string;
  admin_password_placeholder: string;
  admin_password_error: string;
  admin_logout: string;
  admin_db_tasks: string;
  admin_filling_stats: string;
  admin_tips_list: string;
  admin_create_tip: string;
  admin_edit_tip: string;
  attach_to_tree: string;
  detach_from_tree: string;
  admin_edit_translation: string;
  admin_users: string;
  admin_translate_from_your_current_language: string;
  admin_translate_from_main_admin_language: string;
  show_details: string;
  language: string;
  create: string;
  edit: string;
  duplicate_and_edit: string;
  delete: string;
  save: string;
  cancel: string;
  success: string;
  admin_editing_now: string;
  admin_this_language_is_main_for_admins: string;
  admin_read_only: string;
  admin_translated: string;
  admin_not_translated: string;
  admin_title_from: string;
  admin_title_to: string;
  admin_total: string;
  admin_stage_2: string;
  admin_stage_3: string;
  admin_stage_4: string;
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

export interface FavoritesItem {
  id: number;
  rank_for_language: string;
  title_for_language: string;
  image_url: string;
  leaves_count: number;
}

export interface SearchItem {
  id: number;
  page_url: string;
  rank_for_language: string;
  title_for_language: string;
  image_url: string;
  rank_order: number;
  leaves_count: number;
}
