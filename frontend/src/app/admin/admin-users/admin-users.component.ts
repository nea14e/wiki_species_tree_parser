import { Component, OnInit } from '@angular/core';
import {AdminLanguage, AdminUser} from '../models-admin';
import {RootDataKeeperService} from '../../root-data-keeper.service';
import {AdminUsersNetworkService} from './admin-users-network.service';

@Component({
  selector: 'app-admin-users',
  templateUrl: './admin-users.component.html',
  styleUrls: [
    './admin-users.component.css',
    '../../app.component.css'
  ]
})
export class AdminUsersComponent implements OnInit {

  LIST_AUTORELOAD_INTERVAL = 2000;  // TODO remove it
  autoReloadTimeoutId: number | null = null;

  users: AdminUser[] = [];
  isTestDb: boolean | null = null;
  editingUser: AdminUser | null = null;
  knownLanguagesAll: AdminLanguage[] = [];

  balloonMessage: string | null = null;
  balloonTimeoutId: number | null = null;

  constructor(public rootData: RootDataKeeperService,
              private networkAdminService: AdminUsersNetworkService) { }

  ngOnInit(): void {
    this.reloadList();

    this.networkAdminService.getKnownLanguagesAll(this.rootData.adminPassword).subscribe(data => {
      this.knownLanguagesAll = data;
    }, error => {
      alert(error || this.rootData.translationRoot.translations.network_error);  // пришедший текст ошибки или стандартный
    });
  }

  private reloadList(): void {
    this.networkAdminService.getAdminUsers(this.rootData.adminPassword).subscribe(data => {
      this.users = data.admin_users;
      this.isTestDb = data.is_test_db;
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
    this.editingUser = new AdminUser();
    setTimeout(() => {
      window.scrollTo(0, 9999999);
    }, 250);
  }

  onEditClick(task: AdminUser): void {
    this.editingUser = JSON.parse(JSON.stringify((task)));  // deep copy of object. To can be enabled to cancel changes
    setTimeout(() => {
      window.scrollTo(0, 9999999);
    }, 250);
  }

  onDuplicateClick(task: AdminUser): void {
    this.editingUser = JSON.parse(JSON.stringify((task)));  // deep copy of object. Copying of object.
    this.editingUser.id = null;  // mark task as new
    setTimeout(() => {
      window.scrollTo(0, 9999999);
    }, 250);
  }

  onDeleteClick(task: AdminUser): void {
    if (!confirm('Delete admin user?')) {
      return;
    }
    this.networkAdminService.deleteAdminUser(task.id, this.rootData.adminPassword).subscribe(adminResponse => {
      this.showBalloon(adminResponse.message);
      this.reloadList();
    }, error => {
      alert(error || this.rootData.translationRoot.translations.network_error);  // пришедший текст ошибки или стандартный
    });
  }

  onCancelClick(): void {
    this.editingUser = null;
  }

  onSaveClick(): void {
    if (!this.editingUser.id) {
      this.networkAdminService.createAdminUser(this.editingUser, this.rootData.adminPassword).subscribe(adminResponse => {
        this.showBalloon(adminResponse.message);
        this.editingUser = null;
        this.reloadList();
      }, error => {
        alert(error || this.rootData.translationRoot.translations.network_error);  // пришедший текст ошибки или стандартный
      });
    } else {
      this.networkAdminService.saveAdminUser(this.editingUser, this.rootData.adminPassword).subscribe(adminResponse => {
        this.showBalloon(adminResponse.message);
        this.editingUser = null;
        this.reloadList();
      }, error => {
        alert(error || this.rootData.translationRoot.translations.network_error);  // пришедший текст ошибки или стандартный
      });
    }
  }

  getColorForAdminUser(task: AdminUser): string {
    if (task.is_blocked === true) {
      return '#f57c7c';
    }
    return '#ffffff00';
  }
}
