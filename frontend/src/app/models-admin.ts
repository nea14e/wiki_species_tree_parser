export class DbTask {
  id: number | null;
  stage: string;
  args: string;
  isRunOnStartup = true;
  isCompleted = false;
}

export class AdminResponse {
  isOk: boolean;
  message: string;
}
