import {TranslationsByLanguages} from './translations-by-languages';

export class TipForTranslation {
  id!: number;
  tip_on_languages!: TranslationsByLanguages;
  species_id!: number;
  page_url!: string;
  image_url!: string;
  titles_by_languages!: TranslationsByLanguages;
  wikipedias_by_languages!: TranslationsByLanguages;
  title_by_latin!: string;
  title_by_admin!: string;
  title_by_language!: string;
  rank_by_admin!: string;
  rank_by_language!: string;
}
