import {Component, OnInit} from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {NetworkDbTasksService} from "../db-tasks/network-db-tasks.service";
import {NetworkFillingStatsService} from "./network-filling-stats.service";
import {FillingStatsItem} from "../../models-admin";

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

  constructor(public activatedRoute: ActivatedRoute,
              private networkAdminService: NetworkFillingStatsService) { }

  ngOnInit(): void {
    this.activatedRoute.queryParams.subscribe(params => {
      // Эта лямбда будет вызвана автоматически при любых изменениях параметров адреса в браузереNumber
    // this.groupNumber = +this.params.groupNumber || null;
    // Приводим к числу с помощью + или, если в адресе не указан параметр groupNumber, то null.
    // this.nestedLevel = +this.params.nestedLevel || 0;
    // Приводим к числу с помощью + или, если в адресе не указан параметр nestedLevel, то 0.
    });
    this.reload();
  }

  public reload(): void {
    this.networkAdminService.getFillingStats(this.groupsCount, this.nestedLevel, this.outerGroupNumber, this.isTestData).subscribe(data => {
      this.items = data.stats;
      this.isTestDb = data.is_test_db;
      console.log('Данные' + data);
    }, error => {
      alert(error);
    });
  }

  onGroupsCountChanged(e): void {
    this.groupsCount = e.target.value;
  }
}
