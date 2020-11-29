import { Component, OnInit } from '@angular/core';
import {NetworkAdminService} from '../../network-admin.service';
import {RootDataKeeperService} from "../../root-data-keeper.service";
import {DbTask} from "../../models-admin";

@Component({
  selector: 'app-db-tasks',
  templateUrl: './db-tasks.component.html',
  styleUrls: ['./db-tasks.component.css']
})
export class DbTasksComponent implements OnInit {

  tasks: DbTask[] = [];

  constructor(public rootData: RootDataKeeperService,
              private networkAdminService: NetworkAdminService) { }

  ngOnInit(): void {
    this.networkAdminService.getDbTasks(this.rootData.adminPassword).subscribe(data => {
      this.tasks = data;
    }, error => {
      alert(error || this.rootData.translationRoot.translations.network_error);  // пришедший текст ошибки или стандартный
    });
  }

}
