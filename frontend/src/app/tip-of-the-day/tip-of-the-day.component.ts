import {Component, OnInit} from '@angular/core';
import {NetworkService} from '../network.service';
import {ActivatedRoute, Router} from '@angular/router';
import {TipOfTheDay} from '../models';
import {RootDataKeeperService} from '../root-data-keeper.service';
import {CopyToClipboardService} from '../copy-to-clipboard.service';

@Component({
  selector: 'app-tip-of-the-day',
  templateUrl: './tip-of-the-day.component.html',
  styleUrls: [
    '../app.component.css',
    './tip-of-the-day.component.css'
  ]
})
export class TipOfTheDayComponent implements OnInit {

  tip: TipOfTheDay;

  constructor(public rootData: RootDataKeeperService,
              private networkService: NetworkService,
              private activatedRoute: ActivatedRoute,
              private router: Router,
              private copyToClipboardService: CopyToClipboardService) {
  }

  ngOnInit(): void {
    this.activatedRoute.queryParams.subscribe(params => {
      this.rootData.lastTipParams = params;
      const id: number = +params.id || null;
      this.loadTip(id);
    });
  }

  loadTip(id: number): void {
    if (!!id) {
      this.networkService.getTipOfTheDayById(id).subscribe(data => {
        const isFirstTip = (!this.tip);
        this.tip = data;
        this.router.navigate(['tip'], {queryParams: {id: this.tip.id}, replaceUrl: isFirstTip});
      }, () => {
        alert(this.rootData.translationRoot.translations.network_error);
      });
    } else {
      this.networkService.getTipOfTheDay().subscribe(data => {
        const isFirstTip = (!this.tip);
        this.tip = data;
        this.router.navigate(['tip'], {queryParams: {id: this.tip.id}, replaceUrl: isFirstTip});
      }, () => {
        alert(this.rootData.translationRoot.translations.network_error);
      });
    }
  }

  isShowInTreeDisabled(): boolean {
    return !this.tip || !this.tip.species_id;
  }

  onShowInTreeClick(): void {
    this.router.navigate(['tree'], {queryParams: {id: this.tip.species_id}});
  }

  onNextTipClick(): void {
    this.loadTip(null);
  }

  // noinspection JSMethodCanBeStatic
  onShareClick(): void {
    const val = window.location.href;
    this.copyToClipboardService.copy(val);
    alert(this.rootData.translationRoot?.translations.link_copied);
  }

  onToTreeClick(): void {
    if (!!this.rootData.lastTreeParams) {
      this.router.navigate(['tree'], {queryParams: this.rootData.lastTreeParams});
    } else {
      this.router.navigate(['tree']);
    }
  }
}
