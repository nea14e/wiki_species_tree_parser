import {Component, OnInit} from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import {NetworkFillingStatsService} from './network-filling-stats.service';
import {FillingStatsItem} from '../../models-admin';
import {RootDataKeeperService} from "../../root-data-keeper.service";

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
  isTestData = true;
  items: FillingStatsItem[] = [];
  isTestDb: boolean;

  constructor(public rootData: RootDataKeeperService,
              public activatedRoute: ActivatedRoute,
              private networkAdminService: NetworkFillingStatsService,
              private router: Router) { }

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
    this.networkAdminService.getFillingStats(this.groupsCount, this.nestedLevel, this.outerGroupNumber, this.isTestData).subscribe(data => {
      this.items = data.stats;
      this.isTestDb = data.is_test_db;
      console.log('Данные', data);
    }, error => {
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
    this.router.navigate(['admin/filling-stats'], {queryParams: {outerGroupNumber: item.group_number, nestedLevel: this.nestedLevel + 1}});
  }

  home(): void {
    // noinspection JSIgnoredPromiseFromCall
    this.router.navigate(['admin/filling-stats']);
  }
}
