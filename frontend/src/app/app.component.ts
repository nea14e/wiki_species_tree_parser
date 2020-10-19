import {Component, OnInit} from '@angular/core';
import {NetworkService} from './network.service';
import {Item, Level, TranslationRoot, Tree} from './models';
import {ActivatedRoute, Router} from '@angular/router';
import {RootDataKeeperService} from './root-data-keeper.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {

  translationRoot: TranslationRoot;

  constructor(public rootData: RootDataKeeperService,
              private networkService: NetworkService,
              private activatedRoute: ActivatedRoute,
              private router: Router) {}

  ngOnInit(): void {
    this.networkService.getTranslations().subscribe(data => {
      this.translationRoot = data;
      this.rootData.translationRoot = data;
    }, error => {
      alert(error);
    });
  }

  onTipClick(): void {
    if (!!this.rootData.lastTipParams) {
      this.router.navigate(['tip'], {queryParams: this.rootData.lastTipParams});
    } else {
      this.router.navigate(['tip']);
    }
  }

  onToTreeRootClick(): void {
    if (!!this.rootData.lastTreeParams) {
      this.router.navigate(['tree'], {queryParams: this.rootData.lastTreeParams});
    } else {
      this.router.navigate(['tree']);
    }
  }

  onSearchClick(): void {
    if (!!this.rootData.lastSearchParams) {
      this.router.navigate(['search'], {queryParams: this.rootData.lastSearchParams});
    } else {
      this.router.navigate(['search']);
    }
  }

  onAuthorsClick(): void {
    this.router.navigate(['authors']);
  }
}
