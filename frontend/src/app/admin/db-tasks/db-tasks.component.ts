import { Component, OnInit } from '@angular/core';
import {NetworkAdminService} from '../network-admin.service';
import {RootDataKeeperService} from '../../root-data-keeper.service';
import {AdminLanguage, DbTask} from '../models-admin';

@Component({
  selector: 'app-db-tasks',
  templateUrl: './db-tasks.component.html',
  styleUrls: [
    './db-tasks.component.css',
    '../../app.component.css'
  ]
})
export class DbTasksComponent implements OnInit {

  LIST_AUTORELOAD_INTERVAL = 2000;
  autoReloadTimeoutId: number | null = null;

  tasks: DbTask[] = [];
  isTestDb: boolean | null = null;
  editingTask: DbTask | null = null;
  logShowingTaskId: number | null = null;
  logShowingTask: DbTask | null = null;
  logShowingAutoScroll = true;
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
      this.tasks = data.tasks;
      this.isTestDb = data.is_test_db;
      this.updateShowedLog();
      if (!!this.autoReloadTimeoutId) {
        clearTimeout(this.autoReloadTimeoutId);
      }
      this.autoReloadTimeoutId = setTimeout(() => {
        this.reloadList();
      }, this.LIST_AUTORELOAD_INTERVAL);  // обновлять список каждые несколько секунд
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
    setTimeout(() => {
      window.scrollTo(0, 9999999);
    }, 250);
  }

  onEditClick(task: DbTask): void {
    this.editingTask = JSON.parse(JSON.stringify((task)));  // deep copy of object. To can be enabled to cancel changes
    setTimeout(() => {
      window.scrollTo(0, 9999999);
    }, 250);
  }

  onDuplicateClick(task: DbTask): void {
    this.editingTask = JSON.parse(JSON.stringify((task)));  // deep copy of object. Copying of object.
    this.editingTask.id = null;  // mark task as new
    setTimeout(() => {
      window.scrollTo(0, 9999999);
    }, 250);
  }

  setTaskRerunDefaults(task: DbTask): void {
    task.is_rerun_on_startup = this.isTaskRerunEnabled(task);
    task.is_resume_on_startup = this.isTaskResumeEnabled(task);
  }

  isTaskRerunEnabled(task: DbTask): boolean {
    return task.stage === '0' || task.stage === 'test_task';
  }

  isTaskResumeEnabled(task: DbTask): boolean {
    return task.stage === '2' || task.stage === 'parse_language';
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

  getTaskResumeState(task: DbTask): string {
    if (task.is_rerun_on_startup) {
      return 'Rerun';
    }
    if (task.is_resume_on_startup) {
      return 'Resume';
    }
    return '';
  }

  onStartClick(task: DbTask): void {
    this.networkAdminService.startOneTask(task, this.rootData.adminPassword).subscribe(adminResponse => {
      this.showBalloon(adminResponse.message);
      this.logShowingAutoScroll = true;
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

  onShowLogClick(task: DbTask): void {
    this.logShowingTaskId = task.id;
    this.logShowingTask = task;
    this.logShowingAutoScroll = true;
    setTimeout(() => {
      window.scrollTo(0, 9999999);
    }, 250);
  }

  private updateShowedLog(): void {
    if (!this.logShowingTaskId) {
      this.logShowingTask = null;
      return;
    }

    const task = this.tasks.find(t => t.id === this.logShowingTaskId);
    if (!task) {
      this.logShowingTaskId = null;
      this.logShowingTask = null;
      return;
    }
    const prevTask = this.logShowingTask;
    this.logShowingTask = task;

    if (this.logShowingAutoScroll === true &&
      (prevTask.recent_stdout !== task.recent_stdout ||
      prevTask.recent_stderr !== task.recent_stderr)) {
      setTimeout(() => {
        window.scrollTo(0, 9999999);
      }, 250);
    }
  }

  onLogBackClick(): void {
    this.logShowingTaskId = null;
  }
}
