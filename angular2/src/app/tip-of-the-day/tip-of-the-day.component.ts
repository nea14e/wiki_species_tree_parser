import {Component, computed, inject, OnInit, signal} from '@angular/core';
import {RootDataKeeperService} from '../common/root-data-keeper.service';
import {NETWORK_ERROR_DEFAULT_MESSAGE, NetworkService} from '../network.service';
import {ActivatedRoute, Router} from '@angular/router';
import {CopyToClipboardService} from '../common/copy-to-clipboard.service';
import {TipOfTheDay} from '../models/tip-of-the-day';

@Component({
  selector: 'app-tip-of-the-day',
  templateUrl: './tip-of-the-day.component.html',
  styleUrl: './tip-of-the-day.component.css'
})
export class TipOfTheDayComponent implements OnInit {
  public rootData = inject(RootDataKeeperService);
  private _networkService = inject(NetworkService);
  private _activatedRoute = inject(ActivatedRoute);
  private _router = inject(Router);
  private _copyToClipboardService = inject(CopyToClipboardService);

  tip = signal<TipOfTheDay | null>(null);

  ngOnInit(): void {
    this._activatedRoute.queryParams.subscribe(params => {
      this.rootData.lastTipParams = params;
      const id: number | null = +params['id'] || null;
      this.loadTip(id);
    });
  }

  loadTip(id: number | null): void {
    if (!!id) {
      this._networkService.getTipOfTheDayById(id).subscribe({
        next: data => {
          const isFirstTip = (!this.tip());
          this.tip.set(data);
          this._router.navigate(['tip'], {queryParams: {id: data.id}, replaceUrl: isFirstTip});
        }, error: () => {
          alert(this.rootData.translationRoot()?.translations.network_error || NETWORK_ERROR_DEFAULT_MESSAGE);
        }
      });
    } else {
      this._networkService.getTipOfTheDay().subscribe({
        next: data => {
          const isFirstTip = (!this.tip);
          this.tip.set(data);
          this._router.navigate(['tip'], {queryParams: {id: data.id}, replaceUrl: isFirstTip});
        }, error: () => {
          alert(this.rootData.translationRoot()?.translations.network_error || NETWORK_ERROR_DEFAULT_MESSAGE);
        }
      });
    }
  }

  isShowInTreeDisabled = computed(() => {
    const tip = this.tip();
    return !tip || !tip.species_id;
  });

  onShowInTreeClick(): void {
    this._router.navigate(['tree'], {queryParams: {id: this.tip()!.species_id}});
  }

  onNextTipClick(): void {
    this.loadTip(null);
  }

  // noinspection JSMethodCanBeStatic
  onShareClick(): void {
    const val = window.location.href;
    this._copyToClipboardService.copy(val);
    alert(this.rootData.translationRoot()?.translations.link_copied);
  }

  onToTreeClick(): void {
    if (!!this.rootData.lastTreeParams) {
      this._router.navigate(['tree'], {queryParams: this.rootData.lastTreeParams});
    } else {
      this._router.navigate(['tree']);
    }
  }
}
