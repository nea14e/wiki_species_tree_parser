export interface Item {
  id: number;
  page_url: string;
  image_url: string;
  parent_id: number | null;
  is_expanded: boolean;
  is_selected: boolean;
  leaves_count: number;
  title_latin: string;
  title_for_language: string;
  wiki_url_for_language: string;
}
