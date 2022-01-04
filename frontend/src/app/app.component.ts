import {Component, OnInit} from '@angular/core';
import {NetworkService} from './network.service';
import {TranslationRoot} from './models';
import {ActivatedRoute, Router} from '@angular/router';
import {RootDataKeeperService} from './root-data-keeper.service';
import {Location} from '@angular/common';
import {Title} from '@angular/platform-browser';
import {BaseNetworkAdminService} from './admin/network-admin.service';
import {FavoritesService} from './favorites.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {

  translationRoot: TranslationRoot;
  isAdminMode = false;  // активируется по URL "/admin" и его продолжениям
  adminLoginResult: string | null = null;
  JSON = JSON;

  constructor(public rootData: RootDataKeeperService,
              public favoritesService: FavoritesService,
              private networkService: NetworkService,
              private networkAdminService: BaseNetworkAdminService,
              private activatedRoute: ActivatedRoute,
              private router: Router,
              private location: Location,
              private titleService: Title) {
  }

  ngOnInit(): void {
    this.networkService.getTranslations().subscribe(data => {
      this.translationRoot = data;
      this.rootData.translationRoot = data;
      this.titleService.setTitle(data.translations.site_title);
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

  onToFillingStatsClick(): void {
    this.router.navigate(['admin/filling-stats']);
  }

  onToTipTranslationClick(): void {
    this.router.navigate(['admin/tip-translation']);
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
    this.networkAdminService.tryLogin(this.rootData.adminPassword).subscribe(data => {
      this.isAdminMode = true;
      this.adminLoginResult = this.translationRoot?.translations.admin_welcome_part_1 + data.description;
      this.rootData.adminLoginInfo = data;
      this.adminRedirectWithRights();
    }, error => {
      this.adminLoginResult = error;
      this.rootData.adminLoginInfo = null;
      this.onTipClick();
    });
  }

  private adminRedirectWithRights(): void {
    if (this.rootData.canManageDbTasks()) {
      this.router.navigate(['authors'])  // navigate to some another component previously to refresh db-tasks
        .then(() => this.router.navigate(['admin/db-tasks']));  // Show db tasks admin panel
      return;
    }
    if (this.rootData.canSeeTipTranslation()) {
      this.router.navigate(['authors'])  // navigate to some another component previously to refresh db-tasks
        .then(() => this.router.navigate(['tip-translation']));  // Show db tasks admin panel
      return;
    }
  }

  onFavoritesToggleClick(): void {
    this.favoritesService.toggleTab();
  }
}
