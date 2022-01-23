import {Component, OnInit} from '@angular/core';
import {ActivatedRoute} from '@angular/router';

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
  groupNumber = null;
  nestedLevel = 0;

  constructor(public activatedRoute: ActivatedRoute) { }

  ngOnInit(): void {
    this.activatedRoute.queryParams.subscribe(params => {
      // Эта лямбда будет вызвана автоматически при любых изменениях параметров адреса в браузере
    // this.groupNumber = +this.params.groupNumber || null;
    // Приводим к числу с помощью + или, если в адресе не указан параметр groupNumber, то null.
    // this.nestedLevel = +this.params.nestedLevel || 0;
    // Приводим к числу с помощью + или, если в адресе не указан параметр nestedLevel, то 0.
    });
    this.reload();
  }

  public reload(): void {

  }

  onGroupsCountChanged(e): void {
    this.groupsCount = e.target.value;
  }
}
