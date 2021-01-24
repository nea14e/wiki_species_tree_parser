import { Component, OnInit } from '@angular/core';
import {RootDataKeeperService} from '../../root-data-keeper.service';
import {AdminLanguage, AdminUser, Right, RIGHTS} from '../../models-admin';
import {NetworkAdminUsersService} from './network-admin-users.service';

@Component({
  selector: 'app-admin-users',
  templateUrl: './admin-users.component.html',
  styleUrls: [
    './admin-users.component.css',
    '../../app.component.css'
  ]
})
export class AdminUsersComponent implements OnInit {

  users: AdminUser[] = [];
  editingUser: AdminUser | null = null;
  isTestDb: boolean | null = null;
  knownLanguagesAll: AdminLanguage[] = [];
  RIGHTS = RIGHTS;

  constructor(public rootData: RootDataKeeperService,
              private networkAdminService: NetworkAdminUsersService) { }

  ngOnInit(): void {
    this.reloadList();
    this.loadKnownLanguage();
  }

  private reloadList(): void {
    this.networkAdminService.getAdminUsers(this.rootData.adminPassword).subscribe(data => {
      this.users = data.admin_users;
      this.isTestDb = data.is_test_db;
    }, error => {
      alert(error);
    });
  }

  private loadKnownLanguage(): void {
    this.networkAdminService.getKnownLanguagesAll(this.rootData.adminPassword).subscribe(data => {
      this.knownLanguagesAll = data;
    }, error => {
      alert(error);
    });
  }

  onCreateClick(): void {
    this.users = this.users.filter(u => !!u.id);
    this.editingUser = new AdminUser();
    console.log(this.users);
  }

  getColorForUser(user: AdminUser): string {
    if (this.isEditingUser(user)) {
      return 'lightblue';
    }
    if (user.is_blocked === true) {
      return '#f57c7c';
    }
    return '#ffffff00';
  }

  onEditClick(user: AdminUser): void {
    this.users = this.users.filter(u => !!u.id);
    this.editingUser = JSON.parse(JSON.stringify((user)));  // deep copy of object. To can be enabled to cancel changes
  }

  onSaveClick(): void {
    if (!!this.editingUser.id) {
      this.networkAdminService.saveAdminUser(this.editingUser, this.rootData.adminPassword).subscribe(() => {
        this.editingUser = null;
        this.reloadList();
      }, error => {
        alert(error);
      });
    } else {
      this.networkAdminService.createAdminUser(this.editingUser, this.rootData.adminPassword).subscribe(() => {
        this.editingUser = null;
        this.reloadList();
      }, error => {
        alert(error);
      });
    }
  }

  onDeleteClick(user: AdminUser): void {
    if (!confirm('Delete user?')) {
      return;
    }
    this.networkAdminService.deleteAdminUser(user.id, this.rootData.adminPassword).subscribe(() => {
      this.reloadList();
    }, error => {
      alert(error);
    });
  }

  onCancelClick(): void {
    this.users = this.users.filter(u => !!u.id);
    this.editingUser = null;
  }

  isEditingUser(user: AdminUser): boolean {
    return this.editingUser?.id === user.id;
  }

  onAddRightClick(): void {
    this.editingUser.rights_list.push(new Right(null));
  }

  onDeleteRightClick(ind: number): void {
    this.editingUser.rights_list.splice(ind, 1);
  }
}
