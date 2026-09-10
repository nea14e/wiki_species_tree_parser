import {Component, inject, OnInit} from '@angular/core';
import {FillingStatsItem} from '../models/filling-stats-item';
import {AdminLanguage} from '../models/admin-language';
import {RootDataKeeperService} from '../../common/root-data-keeper.service';
import {ActivatedRoute, Router} from '@angular/router';
import {NetworkFillingStatsService} from './network-filling-stats.service';
import {NgClass, NgStyle} from '@angular/common';
import {FormsModule} from '@angular/forms';

@Component({
  selector: 'app-filling-stats',
  imports: [
    NgClass,
    FormsModule,
    NgStyle
  ],
  templateUrl: './filling-stats.component.html',
  styleUrl: './filling-stats.component.css',
})
export class FillingStatsComponent implements OnInit {

  groupsCount = 20;
  pageUrlFrom: string | null = null;
  pageUrlTo: string | null = null;
  bordersStack: { from: string, to: string }[] = [];
  isTestData = false;
  items: FillingStatsItem[] = [];
  languageKey: string | null = null;
  isTestDb = false;
  isLoading = false;
  knownLanguagesAll: AdminLanguage[] = [];

  rootData = inject(RootDataKeeperService);
  activatedRoute = inject(ActivatedRoute);
  private networkAdminService = inject(NetworkFillingStatsService)
  private router = inject(Router);

  ngOnInit(): void {
    this.activatedRoute.queryParams.subscribe(params => {
      this.pageUrlFrom = params['pageUrlFrom'] || null;
      this.pageUrlTo = params['pageUrlTo'] || null;
      this.reload();
    });
    this.networkAdminService.getKnownLanguagesAll(this.rootData.adminPassword!).subscribe({
      next:
        data => {
          this.knownLanguagesAll = data;
          this.reload();  // первоначальная загрузка только после загрузки списка всех языков
        },
      error: error => {
        alert(error);
      }
    });
  }

  public reload(): void {
    this.isLoading = true;
    this.networkAdminService.getFillingStats(this.pageUrlFrom, this.pageUrlTo, this.groupsCount, this.languageKey, this.isTestData)
      .subscribe({
        next: data => {
          this.isLoading = false;
          this.items = data.stats;
          this.languageKey = data.language_key;
          this.isTestDb = data.is_test_db;
          console.log('Данные', data);
        },
        error: error => {
          this.isLoading = false;
          alert(error);
        }
      });
  }

  onGroupsCountChanged(e: any): void {
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
