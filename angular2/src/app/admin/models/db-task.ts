import {DbTaskArgs} from './db-task-args';

export class DbTask {
  id!: number | null;
  stage!: string;
  python_exe = 'python3';
  args: DbTaskArgs = new DbTaskArgs();
  is_rerun_on_startup!: boolean;
  is_resume_on_startup!: boolean;
  is_launch_now = true;
  is_success = false;
  is_running_now!: boolean;
  recent_stdout!: string;
  recent_stderr!: string;
  is_auto_created = false;

  static getColor(task: DbTask): string {
    if (task.is_running_now) {
      return 'lightblue';
    }
    if (task.is_success === true) {
      return '#a6dca6';
    }
    if (task.is_success === false) {
      return '#f57c7c';
    }
    return 'white';
  }

  static getTaskState(task: DbTask): string {
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

  static getTaskResumeState(task: DbTask): string {
    if (task.is_rerun_on_startup) {
      return 'Rerun';
    }
    if (task.is_resume_on_startup) {
      return 'Resume';
    }
    return '';
  }
}
