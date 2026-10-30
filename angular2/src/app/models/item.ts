export interface Item {
  id: number;
  page_id: string;
  image_url: string;
  parent_id: number | null;
  is_expanded: boolean;
  is_selected: boolean;
  leaves_count: number;
  title_for_language1: string;
  title_for_language2: string;
  title_latin: string;
}
