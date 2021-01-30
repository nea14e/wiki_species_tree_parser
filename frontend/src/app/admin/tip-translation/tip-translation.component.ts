import {Component, OnInit} from '@angular/core';
import {RootDataKeeperService} from '../../root-data-keeper.service';
import {AdminLanguage, AdminMainLanguage, RIGHTS, TipForTranslation} from '../../models-admin';
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
  editingForLanguage: AdminLanguage | null = null;
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
      if (!!this.autoReloadTimeoutId) {
        clearTimeout(this.autoReloadTimeoutId);
      }
      this.autoReloadTimeoutId = setTimeout(() => {
        this.reloadData();
      }, this.LIST_AUTORELOAD_INTERVAL);  // обновлять список каждые несколько секунд
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

  getFromLangShortTitle(): string {
    if (this.rootData.isTranslateFromYourLang === true) {
      return this.rootData.translationRoot?.lang_key + ' - ' + this.rootData.translationRoot?.comment;
    } else {
      return this.rootData.mainAdminLanguage?.lang_key + ' - ' + this.rootData.mainAdminLanguage?.comment;
    }
  }

  getTipShortRank(tip: TipForTranslation): string {
    if (this.rootData.isTranslateFromYourLang === true && !!tip.rank_by_language) {
      return tip.rank_by_language;
    } else {
      return tip.rank_by_admin;
    }
  }

  getTipShortTitle(tip: TipForTranslation): string {
    if (this.rootData.isTranslateFromYourLang === true && !!tip.title_by_language) {
      return tip.title_by_language;
    } else if (!!tip.title_by_admin) {
      return tip.title_by_admin;
    } else {
      return tip.title_by_latin;
    }
  }

  getTipTranslationSource(tip: TipForTranslation): string {
    if (this.rootData.isTranslateFromYourLang === true && !!tip.tip_on_languages[this.rootData.translationRoot?.lang_key]) {
      return tip.tip_on_languages[this.rootData.translationRoot?.lang_key];
    } else if (!!tip.tip_on_languages[this.rootData.mainAdminLanguage?.lang_key]) {
      return tip.tip_on_languages[this.rootData.mainAdminLanguage?.lang_key];
    } else {
      return tip.tip_on_languages.ru || '[No tip source found]';
    }
  }

  onCreateClick(): void {
    this.editingTip = new TipForTranslation();
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
    setTimeout(() => {
      window.scrollTo(0, 9999999);
    }, 250);
  }

  onDeleteClick(tip: TipForTranslation): void {
    if (!confirm('Delete task?')) {
      return;
    }
    this.networkAdminService.deleteTip(tip.id, this.rootData.adminPassword).subscribe(() => {
      alert(this.rootData.translationRoot?.translations.success);
      this.editingTip = null;
      // список обновляется по таймеру
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
  }

  onSaveClick(): void {
    const langKey = this.editingForLanguage !== null
      ? this.editingForLanguage.lang_key
      : (this.rootData.isTranslateFromYourLang === false
        ? this.rootData.mainAdminLanguage?.lang_key
        : this.rootData.translationRoot?.lang_key);

    if (!this.editingTip.id) {
      this.networkAdminService.createTip(
        this.editingTip,
        langKey,
        this.rootData.adminPassword
      ).subscribe(adminResponse => {
        alert(this.rootData.translationRoot?.translations.success);
        this.editingTip = null;
        // список обновляется по таймеру
      }, error => {
        alert(error);
      });
    } else {
      this.networkAdminService.saveTip(
        this.editingTip,
        langKey,
        this.rootData.adminPassword
      ).subscribe(adminResponse => {
        alert(this.rootData.translationRoot?.translations.success);
        this.editingTip = null;
        // список обновляется по таймеру
      }, error => {
        alert(error);
      });
    }
  }

  getPreviewForTipCell(tip: TipForTranslation, lang: AdminLanguage): string {
    if (lang.lang_key === this.rootData.mainAdminLanguage?.lang_key) {
      return !!tip.tip_on_languages[lang.lang_key]
        ? 'V!'
        : 'X!';
    }
    return !!tip.tip_on_languages[lang.lang_key]
      ? 'V'
      : 'X';
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
    return !!tip.tip_on_languages[lang.lang_key]
      ? '#a6dca6'
      : '#f57c7c';
  }

  isEditingTip(tip: TipForTranslation): boolean {
    return this.editingTip?.id === tip.id;
  }
}
