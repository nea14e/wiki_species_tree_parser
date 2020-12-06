import { Component, OnInit } from '@angular/core';
import {NetworkAdminService} from '../../network-admin.service';
import {RootDataKeeperService} from '../../root-data-keeper.service';
import {AdminLanguage, DbTask} from '../../models-admin';

@Component({
  selector: 'app-db-tasks',
  templateUrl: './db-tasks.component.html',
  styleUrls: [
    './db-tasks.component.css',
    '../../app.component.css'
  ]
})
export class DbTasksComponent implements OnInit {

  tasks: DbTask[] = [];
  editingTask: DbTask | null = null;
  knownLanguagesAll: AdminLanguage[] = [];

  constructor(public rootData: RootDataKeeperService,
              private networkAdminService: NetworkAdminService) { }

  ngOnInit(): void {
    this.reloadList();

    this.networkAdminService.getKnownLanguagesAll(this.rootData.adminPassword).subscribe(data => {
      this.knownLanguagesAll = data;
      console.log('this.knownLanguagesAll:', this.knownLanguagesAll);
    }, error => {
      alert(error || this.rootData.translationRoot.translations.network_error);  // пришедший текст ошибки или стандартный
    });
  }

  private reloadList(): void {
    this.networkAdminService.getDbTasks(this.rootData.adminPassword).subscribe(data => {
      this.tasks = data;
    }, error => {
      alert(error || this.rootData.translationRoot.translations.network_error);  // пришедший текст ошибки или стандартный
    });
  }

  onCreateClick(): void {
    this.editingTask = new DbTask();
  }

  onEditClick(task: DbTask): void {
    this.editingTask = task;
    setTimeout(() => {
      window.scrollTo(0, 9999999);
    }, 750);
  }

  onDeleteClick(task: DbTask): void {
    if (!confirm('Delete task?')) {
      return;
    }
    this.networkAdminService.deleteTask(task.id, this.rootData.adminPassword).subscribe(adminResponse => {
      alert(adminResponse.message);
      this.reloadList();
    }, error => {
      alert(error || this.rootData.translationRoot.translations.network_error);  // пришедший текст ошибки или стандартный
    });
  }

  onCancelClick(): void {
    this.editingTask = null;
  }

  onSaveClick(): void {
    if (!this.editingTask.id) {
      this.networkAdminService.createTask(this.editingTask, this.rootData.adminPassword).subscribe(adminResponse => {
        alert(adminResponse.message);
        this.editingTask = null;
        this.reloadList();
      }, error => {
        alert(error || this.rootData.translationRoot.translations.network_error);  // пришедший текст ошибки или стандартный
      });
    } else {
      this.networkAdminService.saveTask(this.editingTask, this.rootData.adminPassword).subscribe(adminResponse => {
        alert(adminResponse.message);
        this.editingTask = null;
        this.reloadList();
      }, error => {
        alert(error || this.rootData.translationRoot.translations.network_error);  // пришедший текст ошибки или стандартный
      });
    }
  }
}
