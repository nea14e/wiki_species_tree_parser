import {Component, computed, inject, signal} from '@angular/core';
import {MatDialogRef} from '@angular/material/dialog';
import {RootDataKeeperService} from '../common/root-data-keeper.service';
import {NETWORK_ERROR_DEFAULT_MESSAGE, NetworkService} from '../network.service';
import {CopyToClipboardService} from '../common/copy-to-clipboard.service';
import {TipOfTheDay} from '../models/tip-of-the-day';
import {Router} from '@angular/router';

@Component({
  selector: 'app-tip-of-the-day-dialog',
  templateUrl: './tip-of-the-day.component.html',
  styleUrl: './tip-of-the-day.component.css'
})
export class TipOfTheDayDialogComponent {
  public rootData = inject(RootDataKeeperService);
  private _networkService = inject(NetworkService);
  private _router = inject(Router);
  private _copyToClipboardService = inject(CopyToClipboardService);
  private _dialogRef = inject(MatDialogRef<TipOfTheDayDialogComponent>);

  tip = signal<TipOfTheDay | null>(null);

  isShowInTreeDisabled = computed(() => {
    const tip = this.tip();
    return !tip || !tip.species_id;
  });

  loadTip(tipId: number | null): void {
    let observable = tipId != null
      ? this._networkService.getTipOfTheDayById(tipId)
      : this._networkService.getTipOfTheDay();
    observable.subscribe({
        next: data => {
          this.tip.set(data);
          this.rootData.lastTipId = data.id;
          console.log("TipOfTheDay: loadTip(): id:", data.id);  // TODO
          this._router.navigate(
            ['tree'],
            {
              queryParams: {tipId: data.id},
              queryParamsHandling: "merge"
            }
          );
        }, error: () => {
          alert(this.rootData.translationRoot()?.translations.network_error || NETWORK_ERROR_DEFAULT_MESSAGE);
        }
      });
  }

  onShowInTreeClick(): void {
    if (this.isShowInTreeDisabled()) {
      return;
    }
    this._router.navigate(
      ['tree'],
      {
        queryParams: {id: this.tip()!.species_id},
        queryParamsHandling: "merge"
      }
    );
    this._dialogRef.close();
  }

  onNextTipClick(): void {
    console.log("TipOfTheDay: onNextTipClick()");  // TODO
    this.loadTip(null);
  }

  onShareClick(): void {
    const val = window.location.href;
    this._copyToClipboardService.copy(val);
    alert(this.rootData.translationRoot()?.translations.link_copied);
  }

  onCloseClick(): void {
    this._dialogRef.close();
  }
}
