import {Component, inject, OnInit, signal} from '@angular/core';
import {RootDataKeeperService} from '../../../common/root-data-keeper.service';
import {TipForTranslation} from '../../models/tip-for-translation';
import {MatDialogRef} from '@angular/material/dialog';
import {NetworkTipTranslationService} from '../network-tip-translation.service';
import {ToastrService} from 'ngx-toastr';
import {FormsModule} from '@angular/forms';
import {firstValueFrom, tap} from 'rxjs';

@Component({
  selector: 'app-edit-tip-translation.component',
  imports: [
    FormsModule
  ],
  templateUrl: './edit-tip-translation.component.html',
  styleUrl: './edit-tip-translation.component.css',
})
export class EditTipTranslationComponent implements OnInit {

  private _tip = signal<TipForTranslation>(null!);
  private _originalTip: TipForTranslation = null!;
  tip = this._tip.asReadonly();
  private _langKey1 = signal("");
  langKey1 = this._langKey1.asReadonly();
  private _langKey2 = signal("");
  langKey2 = this._langKey2.asReadonly();

  private _onSavedCallback!: (savedTip: TipForTranslation) => void;

  rootData = inject(RootDataKeeperService);
  private _networkService = inject(NetworkTipTranslationService);
  private _dialogRef = inject(MatDialogRef<EditTipTranslationComponent>);
  private _toastService = inject(ToastrService);

  ngOnInit() {
    this._langKey1.set(this.rootData.selectedLanguageKey1() ?? "ru");
  }

  setCallerData(tip: TipForTranslation, langKey2: string, onSavedCallback: (savedTip: TipForTranslation) => void) {
    const tipClone = JSON.parse(JSON.stringify(tip)) as TipForTranslation;
    this._tip.set(tipClone);
    this._originalTip = JSON.parse(JSON.stringify(tip)) as TipForTranslation;

    this._langKey2.set(langKey2);

    this._onSavedCallback = onSavedCallback;
  }

  setLang1(langKey1: string) {
    this._langKey1.set(langKey1);
  }

  async onCancelClick() {
    if (JSON.stringify(this._tip()) !== JSON.stringify(this._originalTip)) {
      if (confirm(this.rootData.translationRoot()?.translations.confirm_save)) {
        await this.onSaveClick();
        return;
      }
    }
    this._dialogRef.close();
  }

  async onSaveClick() {
    if (!this._tip() || !this._langKey2()) {
      return;
    }
    if (JSON.stringify(this._tip()) === JSON.stringify(this._originalTip)) {
      this._dialogRef.close();
      return;
    }

    const langKey = this._langKey2();
    const tipId = this._tip().id;
    let translationOnLang = this._tip().tip_on_languages[langKey];
    if (!translationOnLang) {
      translationOnLang = "";
    }
    const adminKey = this.rootData.adminPassword;
    if (!adminKey) {
      this._toastService.error(this.rootData.translationRoot()?.translations.admin_password_error);
      return;
    }

    await firstValueFrom(this._networkService.saveTipTranslation(langKey, tipId, translationOnLang, adminKey)
      .pipe(
        tap({
          error: error => {
            this._toastService.error(error.message);
          }
        })
      )
    );

    if (!!this._onSavedCallback) {
      this._onSavedCallback(this.tip());
    }

    this._dialogRef.close();
  }

  autoGrowTextArea($event: any) {
    $event.target.style.height = '0px';
    $event.target.style.height = ($event.target.scrollHeight + 25) + 'px';
  }
}
