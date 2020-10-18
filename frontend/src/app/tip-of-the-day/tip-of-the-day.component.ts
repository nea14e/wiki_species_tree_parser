import {Component, OnInit} from '@angular/core';
import {NetworkService} from '../network.service';
import {ActivatedRoute, Router} from '@angular/router';
import {TipOfTheDay} from '../models';
import {RootDataKeeperService} from '../root-data-keeper.service';

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
              private router: Router) {
  }

  ngOnInit(): void {
    this.loadTip();
  }

  loadTip(): void {
    this.networkService.getTipOfTheDay().subscribe(data => {
      this.tip = data;
      this.router.navigate(['tip'], {queryParams: {id: this.tip.id}});
    }, error => {
      alert(error);
    });
  }

  isShowInTreeDisabled(): boolean {
    return !this.tip || !this.tip.species_id;
  }

  onShowInTreeClick(): void {
    this.router.navigate(['tree'], {queryParams: {id: this.tip.species_id}});
  }

  onNextTipClick(): void {
    this.loadTip();
  }

  onShareClick(): void {
    // TODO
  }

  onToTreeRootClick(): void {
    this.router.navigate(['tree']);
  }
}
