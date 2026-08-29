import {Component, inject, OnInit, signal} from '@angular/core';
import {Tree} from '../models/tree';
import {LatinModeEnum} from '../models/latin-mode-enum';
import {RootDataKeeperService} from '../common/root-data-keeper.service';
import {NETWORK_ERROR_DEFAULT_MESSAGE, NetworkService} from '../network.service';
import {ActivatedRoute, Router} from '@angular/router';
import {CopyToClipboardService} from '../common/copy-to-clipboard.service';
import {FavoritesService} from '../common/favorites.service';
import {Item} from '../models/item';
import {Level} from '../models/level';
import {FormsModule} from '@angular/forms';

@Component({
  selector: 'app-tree.component',
  imports: [
    FormsModule
  ],
  templateUrl: './tree.component.html',
  styleUrl: './tree.component.css',
})
export class TreeComponent implements OnInit {

  public rootData = inject(RootDataKeeperService);
  private _networkService = inject(NetworkService);
  private _activatedRoute = inject(ActivatedRoute);
  private _router = inject(Router);
  private _copyToClipboardService = inject(CopyToClipboardService);
  public favoritesService = inject(FavoritesService);

  tree = signal<Tree | null>(null);
  latinMode: LatinModeEnum = LatinModeEnum.TranslatedOnly;
  LATIN_MODE_ENUM = LatinModeEnum;

  ngOnInit(): void {
    this._activatedRoute.queryParams.subscribe(params => {
      console.log(params);
      this.rootData.lastTreeParams = params;
      const id = +params['id'] || null;
      if (!id) {
        this._networkService.getTreeDefault().subscribe({
          next: (data) => {
            this.tree.set(data);
          }, error: () => {
            alert(this.rootData.translationRoot()?.translations.network_error || NETWORK_ERROR_DEFAULT_MESSAGE);
          }
        });
      } else {
        this._networkService.getTreeById(id).subscribe({
          next: (data) => {
            this.tree.set(data);
          }, error: () => {
            alert(this.rootData.translationRoot()?.translations.network_error || NETWORK_ERROR_DEFAULT_MESSAGE);
          }
        });
      }
    });
  }

  // noinspection JSMethodCanBeStatic
  getItemClass(item: Item): string {
    if (item.is_selected === true) {
      return 'selected';
    } else if (item.is_expanded === true) {
      return 'expanded';
    }
    return '';
  }

  onItemClick(item: Item): void {
    let id: number | null;
    if (item.is_selected) {
      id = item.parent_id;
    } else {
      id = item.id;
    }
    if (!id) {
      this._router.navigate(['tree']);
    } else {
      this._router.navigate(['tree'], {queryParams: {id}});
    }
  }

  // noinspection JSMethodCanBeStatic
  getLevelClass(level: Level): string {
    if (level.is_level_has_selected_item) {
      return 'has-selected';
    }
    return '';
  }

  canReadWiki(item: Item): boolean {
    return !!item.wiki_url_for_language;
  }

  onReadWikiClick(item: Item): void {
    const url = 'https://' + this.tree()?._language_key + '.ruwiki.ru/wiki/' + item.wiki_url_for_language;
    window.open(url, '_blank');
  }

  onYandexItemClick(item: Item): void {
    const url = 'https://yandex.ru/search/?text=' + encodeURIComponent(item.title_for_language);
    window.open(url, '_blank');
  }

  onShareItemClick(_: Item): void {
    const val = window.location.href;
    this._copyToClipboardService.copy(val);
    alert(this.rootData.translationRoot()?.translations.link_copied);
  }

  onToTreeRootClick(): void {
    this._router.navigate(['tree']);
  }

  onFavoritesItemClick(item: Item): void {
    if (!this.favoritesService.hasCookie()) {
      if (!confirm(this.rootData.translationRoot()?.translations.favorites_use_cookies_question)) {
        return;
      }
    }
    this.favoritesService.addItem(item);
  }

  onUnFavoritesItemClick(item: Item): void {
    this.favoritesService.deleteItem(item.id);
  }
}
