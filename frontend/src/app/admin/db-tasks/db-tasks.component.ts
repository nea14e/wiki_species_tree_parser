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

  balloonMessage: string | null = null;
  balloonTimeoutId: number | null = null;

  constructor(public rootData: RootDataKeeperService,
              private networkAdminService: NetworkAdminService) { }

  ngOnInit(): void {
    this.reloadList();

    this.networkAdminService.getKnownLanguagesAll(this.rootData.adminPassword).subscribe(data => {
      this.knownLanguagesAll = data;
    }, error => {
      alert(error || this.rootData.translationRoot.translations.network_error);  // пришедший текст ошибки или стандартный
    });
  }

  private reloadList(): void {
    this.networkAdminService.getDbTasks(this.rootData.adminPassword).subscribe(data => {
      this.tasks = data;
      setTimeout(() => { this.reloadList(); }, 3000);  // обновлять список каждые несколько секунд
    }, error => {
      alert(error || this.rootData.translationRoot.translations.network_error);  // пришедший текст ошибки или стандартный
    });
  }

  private showBalloon(text: string): void {
    this.balloonMessage = text;
    if (this.balloonTimeoutId) {
      clearTimeout(this.balloonTimeoutId);
    }
    this.balloonTimeoutId = setTimeout(
      () => {
        this.balloonMessage = null;
      },
      10000
    );
  }

  onCreateClick(): void {
    this.editingTask = new DbTask();
  }

  onEditClick(task: DbTask): void {
    this.editingTask = JSON.parse(JSON.stringify((task)));  // deep copy of object. To can be enabled to cancel changes
    setTimeout(() => {
      window.scrollTo(0, 9999999);
    }, 500);
  }

  onDuplicateClick(task: DbTask): void {
    this.editingTask = JSON.parse(JSON.stringify((task)));  // deep copy of object. Copying of object.
    this.editingTask.id = null;  // mark task as new
    this.editingTask.is_run_on_startup = true;
    this.editingTask.is_launch_now = true;
    setTimeout(() => {
      window.scrollTo(0, 9999999);
    }, 500);
  }

  onDeleteClick(task: DbTask): void {
    if (!confirm('Delete task?')) {
      return;
    }
    this.networkAdminService.deleteTask(task.id, this.rootData.adminPassword).subscribe(adminResponse => {
      this.showBalloon(adminResponse.message);
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
        this.showBalloon(adminResponse.message);
        this.editingTask = null;
        this.reloadList();
      }, error => {
        alert(error || this.rootData.translationRoot.translations.network_error);  // пришедший текст ошибки или стандартный
      });
    } else {
      this.networkAdminService.saveTask(this.editingTask, this.rootData.adminPassword).subscribe(adminResponse => {
        this.showBalloon(adminResponse.message);
        this.editingTask = null;
        this.reloadList();
      }, error => {
        alert(error || this.rootData.translationRoot.translations.network_error);  // пришедший текст ошибки или стандартный
      });
    }
  }

  getColorForTask(task: DbTask): string {
    if (task.is_running_now) {
      return 'lightblue';
    }
    if (task.is_success === true) {
      return '#a6dca6';
    }
    if (task.is_success === false) {
      return '#f57c7c';
    }
  }

  getTaskState(task: DbTask): string {
    if (task.is_running_now) {
      return 'Running';
    }
    if (task.is_success === true) {
      return 'Ended with success';
    }
    if (task.is_success === false) {
      return 'Ended with error';
    }
  }

  onStartClick(task: DbTask): void {
    this.networkAdminService.startOneTask(task, this.rootData.adminPassword).subscribe(adminResponse => {
      this.showBalloon(adminResponse.message);
      this.reloadList();
    }, error => {
      alert(error || this.rootData.translationRoot.translations.network_error);  // пришедший текст ошибки или стандартный
    });
  }

  onPauseClick(task: DbTask): void {
    this.networkAdminService.stopOneTask(task.id, this.rootData.adminPassword).subscribe(adminResponse => {
      this.showBalloon(adminResponse.message);
      this.reloadList();
    }, error => {
      alert(error || this.rootData.translationRoot.translations.network_error);  // пришедший текст ошибки или стандартный
    });
  }

  onStopClick(task: DbTask): void {
    if (!confirm('Stop this task? Tasks of this stage can\'t be resumed.')) {
      return;
    }

    this.networkAdminService.stopOneTask(task.id, this.rootData.adminPassword).subscribe(adminResponse => {
      this.showBalloon(adminResponse.message);
      this.reloadList();
    }, error => {
      alert(error || this.rootData.translationRoot.translations.network_error);  // пришедший текст ошибки или стандартный
    });
  }
}
