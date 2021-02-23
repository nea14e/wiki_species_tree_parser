import {Component, OnInit} from '@angular/core';
import {NetworkService} from './network.service';
import {TranslationRoot} from './models';
import {ActivatedRoute, Router} from '@angular/router';
import {RootDataKeeperService} from './root-data-keeper.service';
import {Location} from '@angular/common';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {

  translationRoot: TranslationRoot;
  isAdminMode = false;  // активируется по URL "/admin" и его продолжениям

  constructor(public rootData: RootDataKeeperService,
              private networkService: NetworkService,
              private activatedRoute: ActivatedRoute,
              private router: Router,
              private location: Location) {}

  ngOnInit(): void {
    this.networkService.getTranslations().subscribe(data => {
      this.translationRoot = data;
      this.rootData.translationRoot = data;
    }, () => {
      alert('Please check network or try again later.');  // Здесь переводы ещё не загружены, поэтому английский.
      // В остальных местах испрользуйте alert(this.rootData.translationRoot.translations.network_error);
    });

    this.location.onUrlChange(url => {
      if (url.includes('admin')) {
        this.isAdminMode = true;
      }
    });
  }

  onTipClick(): void {
    if (!!this.rootData.lastTipParams) {
      this.router.navigate(['tip'], {queryParams: this.rootData.lastTipParams});
    } else {
      this.router.navigate(['tip']);
    }
  }

  onToTreeClick(): void {
    if (!!this.rootData.lastTreeParams) {
      this.router.navigate(['tree'], {queryParams: this.rootData.lastTreeParams});
    } else {
      this.router.navigate(['tree']);
    }
  }

  onSearchClick(): void {
    if (!!this.rootData.lastSearchParams) {
      this.router.navigate(['search'], {queryParams: this.rootData.lastSearchParams});
    } else {
      this.router.navigate(['search']);
    }
  }

  onAuthorsClick(): void {
    this.router.navigate(['authors']);
  }

  onBackClick(): void {
    this.location.back();
  }

  onForwardClick(): void {
    this.location.forward();
  }

  onToDbTasksClick(): void {
    this.router.navigate(['admin/db-tasks']);
  }

  onToAdminUsersClick(): void {
    this.router.navigate(['admin/admin-users']);
  }

  adminLogout(): void {
    this.isAdminMode = false;
    this.rootData.adminPassword = null;
    this.router.navigate(['tip']);
  }

  onAdminPasswordChange(): void {
    this.router.navigate(['authors'])  // navigate to some another component previously to refresh db-tasks
      .then(() => this.router.navigate(['admin/db-tasks']));  // Show db tasks admin panel
  }
}
