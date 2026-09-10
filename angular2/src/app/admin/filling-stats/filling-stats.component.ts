import {Component, inject, OnInit, signal} from '@angular/core';
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

  groupsCount = signal(20);
  pageUrlFrom = signal<string | null>(null);
  pageUrlTo = signal<string | null>(null);
  bordersStack = signal<{ from: string, to: string }[]>([]);
  isTestData = signal(false);
  items = signal<FillingStatsItem[]>([]);
  languageKey = signal<string | null>(null);
  isTestDb = signal(false);
  isLoading = signal(false);
  knownLanguagesAll = signal<AdminLanguage[]>([]);

  rootData = inject(RootDataKeeperService);
  activatedRoute = inject(ActivatedRoute);
  private networkAdminService = inject(NetworkFillingStatsService)
  private router = inject(Router);

  ngOnInit(): void {
    this.activatedRoute.queryParams.subscribe(params => {
      this.pageUrlFrom.set(params['pageUrlFrom'] || null);
      this.pageUrlTo.set(params['pageUrlTo'] || null);
      this.reload();
    });
    this.networkAdminService.getKnownLanguagesAll(this.rootData.adminPassword!).subscribe({
      next:
        data => {
          this.knownLanguagesAll.set(data);
          this.reload();  // первоначальная загрузка только после загрузки списка всех языков
        },
      error: error => {
        alert(error);
      }
    });
  }

  public reload(): void {
    this.isLoading.set(true);
    this.networkAdminService.getFillingStats(this.pageUrlFrom(), this.pageUrlTo(), this.groupsCount(), this.languageKey(), this.isTestData())
      .subscribe({
        next: data => {
          this.isLoading.set(false);
          this.items.set(data.stats);
          this.languageKey.set(data.language_key);
          this.isTestDb.set(data.is_test_db);
          console.log('Данные', data);
        },
        error: error => {
          this.isLoading.set(false);
          alert(error);
        }
      });
  }

  onGroupsCountChanged(e: any): void {
    this.groupsCount.set(e.target.value);
    this.reload();
  }

  onIsTestDataChanged(): void {
    this.bordersStack.set([]);
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
    const newBorderStack = this.bordersStack();
    newBorderStack.push({from: item.page_url_from, to: item.page_url_to});
    this.bordersStack.set(newBorderStack);
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
    this.bordersStack.set([]);
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
    const newBorderStack = this.bordersStack();
    newBorderStack.splice(newBorderStack.length - 1, 1);
    this.bordersStack.set(newBorderStack);
    if (newBorderStack.length === 0) {
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
    const prevBorders = newBorderStack[newBorderStack.length - 1];
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
