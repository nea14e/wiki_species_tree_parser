import {Component, OnInit} from '@angular/core';
import {RootDataKeeperService} from '../../root-data-keeper.service';
import {AdminLanguage, TipForTranslation} from '../../models-admin';
import {NetworkTipTranslationService} from './network-tip-translation.service';
import {Router} from '@angular/router';

@Component({
  selector: 'app-tip-translation',
  templateUrl: './tip-translation.component.html',
  styleUrls: [
    './tip-translation.component.css',
    '../../app.component.css'
  ]
})
export class TipTranslationComponent implements OnInit {

  LIST_AUTORELOAD_INTERVAL = 2000;
  autoReloadTimeoutId: number | null = null;

  tips: TipForTranslation[] = [];
  editingTip: TipForTranslation | null = null;
  editingLanguage: AdminLanguage | null = null;
  isTestDb: boolean | null = null;
  knownLanguagesAll: AdminLanguage[] = [];

  constructor(public rootData: RootDataKeeperService,
              private networkAdminService: NetworkTipTranslationService,
              private router: Router) {
  }

  ngOnInit(): void {
    this.reloadData();
    this.networkAdminService.getMainAdminLanguage(this.rootData.adminPassword).subscribe(data => {
      this.rootData.mainAdminLanguage = data;
      // список обновляется по таймеру
    }, error => {
      alert(error);
    });
  }

  private reloadData(): void {
    this.networkAdminService.getTipsTranslations(this.rootData.adminPassword).subscribe(data => {
      this.tips = data.tips;
      this.isTestDb = data.is_test_db;
      /*if (!!this.autoReloadTimeoutId) {
        clearTimeout(this.autoReloadTimeoutId);
      }
      this.autoReloadTimeoutId = setTimeout(() => {
        this.reloadData();
      }, this.LIST_AUTORELOAD_INTERVAL);  // обновлять список каждые несколько секунд*/
    }, error => {
      alert(error);
    });
    this.networkAdminService.getKnownLanguagesAll(this.rootData.adminPassword).subscribe(data => {
      this.knownLanguagesAll = data;
      // список обновляется по таймеру
    }, error => {
      alert(error);
    });
  }

  getLangShortTitleFrom(): string {
    if (this.rootData.isTranslateFromYourLang === true) {
      return this.rootData.translationRoot?.lang_key + ' - ' + this.rootData.translationRoot?.comment;
    } else {
      return this.rootData.mainAdminLanguage?.lang_key + ' - ' + this.rootData.mainAdminLanguage?.comment;
    }
  }

  getLangShortTitleTo(): string {
    return this.editingLanguage?.lang_key + ' - ' + this.editingLanguage?.comment;
  }

  getTipShortRank(tip: TipForTranslation): string {
    if (this.rootData.isTranslateFromYourLang === true && !!tip.rank_by_language) {
      return tip.rank_by_language;
    } else {
      return tip.rank_by_admin;
    }
  }

  getTipShortTitleFrom(tip: TipForTranslation): string {
    if (this.rootData.isTranslateFromYourLang === true && !!tip.title_by_language) {
      return tip.title_by_language;
    } else if (!!tip.title_by_admin) {
      return tip.title_by_admin;
    } else if (!!tip.title_by_latin) {
      return tip.title_by_latin;
    } else {
      return '---';
    }
  }

  getTipShortTitleTo(tip: TipForTranslation): string {
    if (!!tip.titles_by_languages && !!tip.titles_by_languages[this.editingLanguage.lang_key]) {
      return tip.titles_by_languages[this.editingLanguage.lang_key];
    } else {
      return '---';
    }
  }

  getTipShortContent(tip: TipForTranslation): string {
    const maxLineLen = 30;
    if (!!tip.page_url) {
      return this.getTipTranslationSource(tip).substring(0, maxLineLen);
    } else {
      const text = this.getTipTranslationSource(tip).substring(0, 4 * maxLineLen);
      // Разбиваем переводами строк по 30 символов длиной
      let result = text.substr(0, maxLineLen) + '<br/>';
      result += text.substr(maxLineLen, maxLineLen) + '<br/>';
      result += text.substr(2 * maxLineLen, maxLineLen) + '<br/>';
      result += text.substr(3 * maxLineLen, maxLineLen) + '<br/>';
      return result;
    }
  }

  getTipTranslationSource(tip: TipForTranslation): string {
    if (this.rootData.isTranslateFromYourLang === true && !!tip.tip_on_languages[this.rootData.translationRoot?.lang_key]) {
      return tip.tip_on_languages[this.rootData.translationRoot?.lang_key];
    } else if (!!tip.tip_on_languages[this.rootData.mainAdminLanguage?.lang_key]) {
      return tip.tip_on_languages[this.rootData.mainAdminLanguage?.lang_key];
    } else if (!!tip.tip_on_languages.ru) {
      return tip.tip_on_languages.ru;
    } else {
      return '---';
    }
  }

  onCreateClick(): void {
    this.editingTip = new TipForTranslation();
    this.editingTip.tip_on_languages = {};
    this.editingTip.page_url = null;
    setTimeout(() => {
      window.scrollTo(0, 9999999);
    }, 250);
  }

  onEditClick(tip: TipForTranslation): void {
    this.editingTip = JSON.parse(JSON.stringify((tip)));  // deep copy of object. To can be enabled to cancel changes
    setTimeout(() => {
      window.scrollTo(0, 9999999);
    }, 250);
  }

  onDuplicateClick(tip: TipForTranslation): void {
    this.editingTip = JSON.parse(JSON.stringify((tip)));  // deep copy of object. Copying of object.
    this.editingTip.id = null;  // mark task as new
    this.editingTip.tip_on_languages = {};
    setTimeout(() => {
      window.scrollTo(0, 9999999);
    }, 250);
  }

  onDeleteClick(tip: TipForTranslation): void {
    if (!confirm(this.rootData.translationRoot?.translations.delete)) {
      return;
    }
    this.networkAdminService.deleteTip(tip.id, this.rootData.adminPassword).subscribe(() => {
      this.editingTip = null;
      this.reloadData();
    }, error => {
      alert(error);
    });
  }

  hasSpeciesAttached(tip: TipForTranslation | null): boolean {
    return !!tip && !!tip.species_id;
  }

  onShowInTreeClick(tip: TipForTranslation): void {
    this.router.navigate(['tree'], {queryParams: {id: tip.species_id}});
  }

  onCancelClick(): void {
    this.editingTip = null;
    this.editingLanguage = null;
  }

  onSaveClick(): void {
    const langKey = this.editingLanguage !== null
      ? this.editingLanguage.lang_key
      : (this.rootData.isTranslateFromYourLang === false
        ? this.rootData.mainAdminLanguage?.lang_key
        : this.rootData.translationRoot?.lang_key);

    if (!this.editingTip.id) {
      this.networkAdminService.createTip(
        this.editingTip,
        langKey,
        this.rootData.adminPassword
      ).subscribe(() => {
        this.editingTip = null;
        this.reloadData();
      }, error => {
        alert(error);
      });
    } else {
      this.networkAdminService.saveTip(
        this.editingTip,
        langKey,
        this.rootData.adminPassword
      ).subscribe(() => {
        this.editingTip = null;
        this.reloadData();
      }, error => {
        alert(error);
      });
    }
  }

  getPreviewForTipCell(tip: TipForTranslation, lang: AdminLanguage): string {
    let result = '';
    if (lang.lang_key === this.rootData.mainAdminLanguage?.lang_key) {
      result = !!tip.tip_on_languages[lang.lang_key] ? 'V!' : 'X!';
    } else {
      result = !!tip.tip_on_languages[lang.lang_key] ? 'V' : 'X';
    }

    if (!this.rootData.canTranslateTipToLanguage(lang.lang_key)) {
      result = '[' + result + ']';
    }
    return result;
  }

  getColorForTipCell(tip: TipForTranslation, lang: AdminLanguage): string {
    if (this.isEditingTip(tip)) {
      return 'lightblue';
    }
    if (lang.lang_key === this.rootData.mainAdminLanguage?.lang_key) {
      return !!tip.tip_on_languages[lang.lang_key]
        ? '#66a366'
        : '#c45050';
    }
    if (!this.rootData.canTranslateTipToLanguage(lang.lang_key)) {
      return !!tip.tip_on_languages[lang.lang_key]
        ? '#9eb89e'
        : '#d2afaf';
    }
    return !!tip.tip_on_languages[lang.lang_key]
      ? '#a6dca6'
      : '#f57c7c';
  }

  isEditingTip(tip: TipForTranslation): boolean {
    return this.editingTip?.id === tip.id;
  }

  onEditTranslationClick(tip: TipForTranslation, lang: AdminLanguage): void {
    this.editingTip = JSON.parse(JSON.stringify((tip)));  // deep copy of object. To can be enabled to cancel changes
    this.editingLanguage = lang;
    setTimeout(() => {
      window.scrollTo(0, 9999999);
    }, 250);
  }

  onSaveTranslationClick(): void {
    this.networkAdminService.saveTipTranslation(
      this.editingLanguage.lang_key,
      this.editingTip.id,
      this.editingTip.tip_on_languages[this.editingLanguage.lang_key],
      this.rootData.adminPassword
    ).subscribe(() => {
      this.editingTip = null;
      this.editingLanguage = null;
      this.reloadData();
    }, error => {
      alert(error);
    });
  }

  autoGrowTextArea(e): void {
    e.target.style.height = '0px';
    e.target.style.height = (e.target.scrollHeight + 25) + 'px';
  }
}
