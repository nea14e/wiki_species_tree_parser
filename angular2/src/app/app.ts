import {Component, inject, OnDestroy, OnInit, signal} from '@angular/core';
import {Router, RouterOutlet} from '@angular/router';
import {TranslationRoot} from './models/translation-root';
import {PagesEnum} from './pages-enum';
import {RootDataKeeperService} from './common/root-data-keeper.service';
import {NETWORK_ERROR_DEFAULT_MESSAGE, NetworkService} from './network.service';
import {Title} from '@angular/platform-browser';
import {BaseNetworkAdminService} from './admin/network-admin.service';
import {Location, NgClass} from '@angular/common';
import {FormsModule} from '@angular/forms';
import {LanguageListItem} from './models/language-list-item';
import {Subscription} from 'rxjs';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, NgClass, FormsModule],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App implements OnInit, OnDestroy {

  public rootData = inject(RootDataKeeperService);
  private networkService = inject(NetworkService);
  private networkAdminService = inject(BaseNetworkAdminService);
  private router = inject(Router);
  private location = inject(Location);
  private titleService = inject(Title);

  languagesList = signal<LanguageListItem[] | []>([]);
  translationRoot = signal<TranslationRoot | null>(null);
  private _languagesChangedSubscription: Subscription | null = null;
  isAdminMode = signal(false);  // активируется по URL "/admin" и его продолжениям
  adminLoginResult = signal<string | null>(null);
  JSON = JSON;
  currentPage = PagesEnum.Tree;
  PagesEnum = PagesEnum;

  ngOnInit(): void {
    this._getLanguagesList();
    this._getTranslations();

    this._languagesChangedSubscription = this.rootData.languagesChangedSubject.subscribe({
      next: _ => {
        this._getTranslations();
      }
    });

    this.location.onUrlChange(url => {
      if (url.includes('admin')) {
        this.isAdminMode.set(true);
      }
      const urlWithoutParams = url.split('?')[0];
      this.currentPage = urlWithoutParams as PagesEnum;
    });
  }

  private _getLanguagesList() {
    this.networkService.getLanguagesList().subscribe({
      next: data => {
        this.languagesList.set(data);
      }, error: () => {
        alert(this.rootData.translationRoot()?.translations.network_error ?? NETWORK_ERROR_DEFAULT_MESSAGE);
      }
    });
  }

  private _getTranslations() {
    const langKey = this.rootData.selectedLanguageKey1();
    this.networkService.getTranslations(langKey).subscribe({
      next: data => {
        this.translationRoot.set(data);
        this.rootData.translationRoot.set(data);
        this.rootData.selectLanguageKey1(data.lang_key);
        this.titleService.setTitle(data.translations.site_title);
      }, error: () => {
        alert(NETWORK_ERROR_DEFAULT_MESSAGE);  // Здесь переводы ещё не загружены, поэтому не переведённое.
        // В остальных местах используйте
        // alert(this.rootData.translationRoot()?.translations.network_error || NETWORK_ERROR_DEFAULT_MESSAGE);
      }
    });
  }

  onTipClick(): void {
    this.router.navigate(
      ['tree'],
      {
        queryParams: {tipId: this.rootData.lastTipId},
        queryParamsHandling: "merge"
      }
    );
  }

  onToTreeClick(): void {
    if (!!this.rootData.lastTreeId) {
      this.router.navigate(
        ['tree'],
        {
          queryParams: {id: this.rootData.lastTreeId},
          queryParamsHandling: "merge"
        });
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
    this.isAdminMode.set(false);
    this.rootData.adminPassword = null;
    this.router.navigate(['tree']);
  }

  onAdminPasswordChange(): void {
    if (!this.rootData.adminPassword) {
      return;
    }
    this.networkAdminService.tryLogin(this.rootData.adminPassword).subscribe({
      next: data => {
        this.isAdminMode.set(true);
        this.adminLoginResult.set(this.translationRoot()?.translations.admin_welcome_part_1 + data.description);
        this.rootData.adminLoginInfo = data;
        this.adminRedirectWithRights();
      }, error: error => {
        this.adminLoginResult.set(error);
        this.rootData.adminLoginInfo = null;
        this.onTipClick();
      }
    });
  }

  private adminRedirectWithRights(): void {
    if (this.rootData.canManageDbTasks()) {
      this.router.navigate(['authors'])  // navigate to some another component previously to refresh db-tasks
        .then(() => this.router.navigate(['admin/db-tasks']));  // Show db tasks admin panel
      return;
    }
    if (this.rootData.canSeeTipTranslation()) {
      this.router.navigate(['authors'])
        .then(() => this.router.navigate(['tip-translation']));
      return;
    }
  }

  ngOnDestroy() {
    this._languagesChangedSubscription?.unsubscribe();
  }
}
