import {Component, inject, OnInit, signal} from '@angular/core';
import {ActivatedRoute, Router, RouterOutlet} from '@angular/router';
import {TranslationRoot} from './models/translation-root';
import {PagesEnum} from './pages-enum';
import {RootDataKeeperService} from './common/root-data-keeper.service';
import {FavoritesService} from './common/favorites.service';
import {NETWORK_ERROR_DEFAULT_MESSAGE, NetworkService} from './network.service';
import {Title} from '@angular/platform-browser';
import {BaseNetworkAdminService} from './admin/network-admin.service';
import {Location, NgClass} from '@angular/common';
import {FormsModule} from '@angular/forms';
import {FavoritesComponent} from './favorites/favorites.component';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, NgClass, FormsModule, FavoritesComponent],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App implements OnInit {

  public rootData = inject(RootDataKeeperService);
  public favoritesService = inject(FavoritesService);
  private networkService = inject(NetworkService);
  private networkAdminService = inject(BaseNetworkAdminService);
  private activatedRoute = inject(ActivatedRoute);
  private router = inject(Router);
  private location = inject(Location);
  private titleService = inject(Title);

  translationRoot = signal<TranslationRoot | null>(null);
  isAdminMode = signal(false);  // активируется по URL "/admin" и его продолжениям
  adminLoginResult = signal<string | null>(null);
  JSON = JSON;
  currentPage = PagesEnum.TipOfTheDay;
  PagesEnum = PagesEnum;

  ngOnInit(): void {
    this.networkService.getTranslations().subscribe({
      next: data => {
        this.translationRoot.set(data);
        this.rootData.translationRoot.set(data);
        this.titleService.setTitle(data.translations.site_title);
      }, error: () => {
        alert(NETWORK_ERROR_DEFAULT_MESSAGE);  // Здесь переводы ещё не загружены, поэтому не переведённое.
        // В остальных местах используйте
        // alert(this.rootData.translationRoot()?.translations.network_error || NETWORK_ERROR_DEFAULT_MESSAGE);
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
    this.isAdminMode.set(false);
    this.rootData.adminPassword = null;
    this.router.navigate(['tip']);
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

  onFavoritesToggleClick(): void {
    this.favoritesService.toggleTab();
  }

  onFavoritesClose() {
    this.favoritesService.isFavoritesOpen.set(false);
  }
}
