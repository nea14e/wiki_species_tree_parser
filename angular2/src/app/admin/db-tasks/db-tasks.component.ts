import {ChangeDetectorRef, Component, computed, inject, OnInit, signal} from '@angular/core';
import {DbTask} from '../models/db-task';
import {AdminLanguage} from '../models/admin-language';
import {RootDataKeeperService} from '../../common/root-data-keeper.service';
import {NetworkDbTasksService} from './network-db-tasks.service';
import {FormsModule} from '@angular/forms';
import {NgClass} from '@angular/common';

@Component({
  selector: 'app-admin-tasks',
  imports: [
    FormsModule,
    NgClass
  ],
  templateUrl: './db-tasks.component.html',
  styleUrl: './db-tasks.component.css',
})
export class DbTasksComponent implements OnInit {

  LIST_AUTORELOAD_INTERVAL = 2000;
  autoReloadTimeoutId: number | null = null;

  rootData = inject(RootDataKeeperService);
  private networkAdminService = inject(NetworkDbTasksService);
  private changeDetectorRef = inject(ChangeDetectorRef);

  tasks = signal<DbTask[]>([]);
  tasksChangeCounter = signal(0);
  tasksWithColor = computed(() => {
    this.tasksChangeCounter();
    console.log('tasksWithColor');
    return this.tasks().map(task => ({...task, color: DbTask.computeColor(task)}));
  });
  isTestDb = signal(false);
  editingTask = signal<DbTask | null>(null);
  logShowingTaskId = signal<number | null>(null);
  logShowingTask = signal<DbTask | null>(null);
  logShowingAutoScroll = signal(true);
  knownLanguagesAll = signal<AdminLanguage[]>([]);

  balloonMessage: string | null = null;
  balloonTimeoutId: number | null = null;

  ngOnInit(): void {
    this.reloadList();

    if (!!this.rootData.adminPassword) {
      this.networkAdminService.getKnownLanguagesAll(this.rootData.adminPassword).subscribe(
        {
          next: data => {
            this.knownLanguagesAll.set(data);
          }, error: error => {
            alert(error);
          }
        });
    }
  }

  private reloadList(): void {
    if (!this.rootData.adminPassword) {
      return;
    }
    this.networkAdminService.getDbTasks(this.rootData.adminPassword).subscribe({
      next: data => {
        this.tasks.set(data.tasks);
        this.tasksChangeCounter.update(n => n + 1);
        this.isTestDb.set(data.is_test_db);
        this.updateShowedLog();
        this.changeDetectorRef.detectChanges();
        if (!!this.autoReloadTimeoutId) {
          clearTimeout(this.autoReloadTimeoutId);
        }
        this.autoReloadTimeoutId = setTimeout(() => {
          this.reloadList();
        }, this.LIST_AUTORELOAD_INTERVAL);  // обновлять список каждые несколько секунд
      }, error: error => {
        alert(error);
      }
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
    this.editingTask.set(new DbTask());
    setTimeout(() => {
      window.scrollTo(0, 9999999);
    }, 250);
  }

  isEditTaskDisabled(task: DbTask): boolean {
    return task.is_auto_created === true;
  }

  onEditClick(task: DbTask): void {
    // Deep copy of object. To can be enabled to cancel changes:
    const clonedTask = JSON.parse(JSON.stringify((task))) as DbTask;
    this.editingTask.set(clonedTask);
    setTimeout(() => {
      window.scrollTo(0, 9999999);
    }, 250);
  }

  onDuplicateClick(task: DbTask): void {
    // Deep copy of object. To can be enabled to cancel changes:
    const clonedTask = JSON.parse(JSON.stringify((task))) as DbTask;
    clonedTask.id = null;  // mark task as new
    this.editingTask.set(clonedTask);
    setTimeout(() => {
      window.scrollTo(0, 9999999);
    }, 250);
  }

  setTaskRerunDefaults(task: DbTask | null): void {
    if (!task) {
      return;
    }
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
    if (!task.id || !this.rootData.adminPassword) {
      return;
    }
    this.networkAdminService.deleteTask(task.id, this.rootData.adminPassword).subscribe({
      next: adminResponse => {
        this.showBalloon(adminResponse.message);
        this.reloadList();
      }, error: error => {
        alert(error);
      }
    });
  }

  onCancelClick(): void {
    this.editingTask.set(null);
  }

  onSaveClick(): void {
    const editingTask = this.editingTask();
    if (!editingTask || !this.rootData.adminPassword) {
      return;
    }
    if (!editingTask.id) {
      this.networkAdminService.createTask(editingTask, this.rootData.adminPassword).subscribe(adminResponse => {
        this.showBalloon(adminResponse.message);
        this.editingTask.set(null);
        this.reloadList();
      }, error => {
        alert(error);
      });
    } else {
      this.networkAdminService.saveTask(editingTask, this.rootData.adminPassword).subscribe(adminResponse => {
        this.showBalloon(adminResponse.message);
        this.editingTask.set(null);
        this.reloadList();
      }, error => {
        alert(error);
      });
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
    return 'Idle';
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
    if (!this.rootData.adminPassword) {
      return;
    }
    this.networkAdminService.startOneTask(task, this.rootData.adminPassword).subscribe({
      next: adminResponse => {
        this.showBalloon(adminResponse.message);
        this.logShowingAutoScroll.set(true);
        this.reloadList();
      }, error: error => {
        alert(error);
      }
    });
  }

  onPauseClick(task: DbTask): void {
    if (!task.id || !this.rootData.adminPassword) {
      return;
    }
    this.networkAdminService.stopOneTask(task.id, this.rootData.adminPassword).subscribe({
      next: adminResponse => {
        this.showBalloon(adminResponse.message);
        this.reloadList();
      }, error: error => {
        alert(error);
      }
    });
  }

  onStopClick(task: DbTask): void {
    if (!confirm('Stop this task? Tasks of this stage can\'t be resumed.')) {
      return;
    }
    this.onPauseClick(task);
  }

  onShowLogClick(task: DbTask): void {
    this.logShowingTaskId.set(task.id);
    this.logShowingTask.set(task);
    this.logShowingAutoScroll.set(true);
    setTimeout(() => {
      window.scrollTo(0, 9999999);
    }, 250);
  }

  private updateShowedLog(): void {
    if (!this.logShowingTaskId()) {
      this.logShowingTask.set(null);
      return;
    }

    const task = this.tasks().find(t => t.id === this.logShowingTaskId());
    if (!task) {
      this.logShowingTaskId.set(null);
      this.logShowingTask.set(null);
      return;
    }
    const prevTask = this.logShowingTask();
    this.logShowingTask.set(task);

    if (this.logShowingAutoScroll() === true &&
      (prevTask?.recent_stdout !== task.recent_stdout ||
        prevTask?.recent_stderr !== task.recent_stderr)) {
      setTimeout(() => {
        window.scrollTo(0, 9999999);
      }, 250);
    }
  }

  onLogBackClick(): void {
    this.logShowingTaskId.set(null);
  }
}
