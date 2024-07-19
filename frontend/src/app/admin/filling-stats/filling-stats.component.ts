import {Component, OnInit} from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import {NetworkFillingStatsService} from './network-filling-stats.service';
import {AdminLanguage, FillingStatsItem} from '../../models-admin';
import {RootDataKeeperService} from '../../root-data-keeper.service';

@Component({
  selector: 'app-filling-stats',
  templateUrl: './filling-stats.component.html',
  styleUrls: [
    './filling-stats.component.css',
    '../../app.component.css'
  ]
})
export class FillingStatsComponent implements OnInit {

  groupsCount = 20;
  pageUrlFrom?: string = null;
  pageUrlTo?: string = null;
  bordersStack: {from: string, to: string}[] = [];
  isTestData = false;
  items: FillingStatsItem[] = [];
  languageKey?: string = null;
  isTestDb: boolean;
  isLoading = false;
  knownLanguagesAll: AdminLanguage[] = [];

  constructor(public rootData: RootDataKeeperService,
              public activatedRoute: ActivatedRoute,
              private networkAdminService: NetworkFillingStatsService,
              private router: Router) { }

  ngOnInit(): void {
    this.activatedRoute.queryParams.subscribe(params => {
      this.pageUrlFrom = params.pageUrlFrom || null;
      this.pageUrlTo = params.pageUrlTo || null;
      this.reload();
    });
    this.networkAdminService.getKnownLanguagesAll(this.rootData.adminPassword).subscribe(data => {
      this.knownLanguagesAll = data;
      this.reload();  // первоначальная загрузка только после загрузки списка всех языков
    }, error => {
      alert(error);
    });
  }

  public reload(): void {
    this.isLoading = true;
    this.networkAdminService.getFillingStats(this.pageUrlFrom, this.pageUrlTo, this.groupsCount, this.languageKey, this.isTestData)
      .subscribe(data => {
        this.isLoading = false;
        this.items = data.stats;
        this.languageKey = data.language_key;
        this.isTestDb = data.is_test_db;
        console.log('Данные', data);
      }, error => {
        this.isLoading = false;
        alert(error);
      });
  }

  onGroupsCountChanged(e): void {
    this.groupsCount = e.target.value;
    this.reload();
  }

  onIsTestDataChanged(): void {
    this.bordersStack = [];
    // noinspection JSIgnoredPromiseFromCall
    this.router.navigate(['admin/filling-stats'],
      {
        queryParams: {
          pageUrlFrom: null,
          pageUrlTo: null
        }
      });
    this.reload();
  }

  onRowClick(item: FillingStatsItem): void {
    if (item.page_url_from === item.page_url_to) {
      return;
    }
    this.bordersStack.push({from: item.page_url_from, to: item.page_url_to});
    // noinspection JSIgnoredPromiseFromCall
    this.router.navigate(['admin/filling-stats'],
      {
        queryParams: {
          pageUrlFrom: item.page_url_from,
          pageUrlTo: item.page_url_to
        }
      });
  }

  home(): void {
    this.bordersStack = [];
    // noinspection JSIgnoredPromiseFromCall
    this.router.navigate(['admin/filling-stats'],
      {
        queryParams: {
          pageUrlFrom: null,
          pageUrlTo: null
        }
      });
  }

  back(): void {
    this.bordersStack.splice(this.bordersStack.length - 1, 1);
    if (this.bordersStack.length === 0) {
      // noinspection JSIgnoredPromiseFromCall
      this.router.navigate(['admin/filling-stats'],
        {
          queryParams: {
            pageUrlFrom: null,
            pageUrlTo: null
          }
        });
      return;
    }
    const prevBorders = this.bordersStack[this.bordersStack.length - 1];
    // noinspection JSIgnoredPromiseFromCall
    this.router.navigate(['admin/filling-stats'],
      {
        queryParams: {
          pageUrlFrom: prevBorders.from,
          pageUrlTo: prevBorders.to
        }
      });
  }
}
