import {Component, OnInit} from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import {NetworkFillingStatsService} from './network-filling-stats.service';
import {FillingStatsItem} from '../../models-admin';
import {RootDataKeeperService} from "../../root-data-keeper.service";
import {Location} from '@angular/common';

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
  outerGroupNumber = null;
  nestedLevel = 0;
  isTestData = false;
  items: FillingStatsItem[] = [];
  isTestDb: boolean;
  isLoading = false;

  constructor(public rootData: RootDataKeeperService,
              public activatedRoute: ActivatedRoute,
              private networkAdminService: NetworkFillingStatsService,
              private router: Router,
              private location: Location) { }

  ngOnInit(): void {
    this.activatedRoute.queryParams.subscribe(params => {
      // Эта лямбда будет вызвана автоматически при любых изменениях параметров адреса в браузереNumber
      this.outerGroupNumber = +params.outerGroupNumber || null;
    // Приводим к числу с помощью + или, если в адресе не указан параметр groupNumber, то null.
      this.nestedLevel = +params.nestedLevel || 0;
    // Приводим к числу с помощью + или, если в адресе не указан параметр nestedLevel, то 0.
      this.reload();
    });
    this.reload();
  }

  public reload(): void {
    this.isLoading = true;
    this.networkAdminService.getFillingStats(this.groupsCount, this.nestedLevel, this.outerGroupNumber, this.isTestData).subscribe(data => {
      this.isLoading = false;
      this.items = data.stats;
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
    this.reload();
  }

  onRowClick(item: FillingStatsItem): void {
    // noinspection JSIgnoredPromiseFromCall
    this.router.navigate(['admin/filling-stats'],
      {
        queryParams: {
          outerGroupNumber: item.group_number,
          nestedLevel: this.nestedLevel + 1
        }
      });
  }

  home(): void {
    // noinspection JSIgnoredPromiseFromCall
    this.router.navigate(['admin/filling-stats']);
  }

  back(): void {
    // noinspection JSIgnoredPromiseFromCall
    this.router.navigate(['admin/filling-stats'],
      {
        queryParams: {
          outerGroupNumber: Math.ceil(this.outerGroupNumber / this.groupsCount),
          nestedLevel: this.nestedLevel - 1
        }
      });
  }
}
