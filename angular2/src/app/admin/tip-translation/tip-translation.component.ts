import {ChangeDetectorRef, Component, inject, OnInit, signal} from '@angular/core';
import {NetworkTipTranslationService} from './network-tip-translation.service';
import {RootDataKeeperService} from '../../common/root-data-keeper.service';
import {NETWORK_ERROR_DEFAULT_MESSAGE} from '../../network.service';
import {TipForTranslation} from '../models/tip-for-translation';
import {Router} from '@angular/router';
import {LanguageListItem} from '../../models/language-list-item';
import {MatDialog} from '@angular/material/dialog';
import {EditTipTranslationComponent} from './edit-tip-translation/edit-tip-translation.component';

@Component({
  selector: 'app-tip-translation.component',
  imports: [],
  templateUrl: './tip-translation.component.html',
  styleUrl: './tip-translation.component.css',
})
export class TipTranslationComponent implements OnInit {

  readonly SHORT_TIP_TEXT_LENGTH = 160;

  isTestDb = signal(false);
  tips = signal<TipForTranslation[]>([]);

  rootData = inject(RootDataKeeperService);
  private _networkService = inject(NetworkTipTranslationService);
  private _changeDetectorRef = inject(ChangeDetectorRef);

  private _router = inject(Router);
  private _dialog = inject(MatDialog);

  ngOnInit() {
    this.reload();
  }

  reload() {
    if (!this.rootData.adminPassword) {
      return;
    }

    this._networkService.getTipsTranslations(this.rootData.adminPassword)
      .subscribe({
        next: result => {
          this.isTestDb.set(result.is_test_db);
          this.tips.set(result.tips);
        }, error: _ => {
          alert(this.rootData.translationRoot()?.translations.network_error || NETWORK_ERROR_DEFAULT_MESSAGE);
        }
      });
  }

  onShowInTreeClick(tip: TipForTranslation) {
    this._router.navigate(
      ['tree'],
      {
        queryParams: {id: tip.species_id}
      }
    );
  }

  getShortTipText(tip: TipForTranslation) {
    const langKey = this.rootData.selectedLanguageKey1();
    const text = tip.tip_on_languages[langKey];
    if (!!text) {
      return text!.substring(0, this.SHORT_TIP_TEXT_LENGTH) +
        (text.length > this.SHORT_TIP_TEXT_LENGTH ? "..." : "");
    }
    return "-";
  }

  getShortTipTranslatedText(tip: TipForTranslation, lang: LanguageListItem) {
    const text = tip.tip_on_languages[lang.lang_key];
    if (!!text) {
      return text!.substring(0, this.SHORT_TIP_TEXT_LENGTH) +
        (text.length > this.SHORT_TIP_TEXT_LENGTH ? "..." : "");
    }
    return "-";
  }

  getLanguageFillingStatus(tip: TipForTranslation, lang: LanguageListItem) {
    if (lang.lang_key in tip.tip_on_languages && !!tip.tip_on_languages[lang.lang_key]) {
      return "V";
    }
    return "X";
  }

  onTipTranslationClick(tip: TipForTranslation, lang: LanguageListItem) {
    const matDialogRef = this._dialog.open(EditTipTranslationComponent, {
      panelClass: 'customized-panel-dialog'
    });
    matDialogRef.componentInstance.setCallerData(tip, lang.lang_key, (savedTip) => {
      tip.tip_on_languages = savedTip.tip_on_languages;
      this._changeDetectorRef.markForCheck();
    });
  }

  getColorForTipCell(tip: TipForTranslation, lang: LanguageListItem) {
    if (!!tip.tip_on_languages[lang.lang_key]) {
      return '#a6dca6';
    } else {
      return '#f57c7c';
    }
  }
}
