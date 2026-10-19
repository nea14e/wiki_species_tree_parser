import {Component, inject, OnDestroy, OnInit, signal} from '@angular/core';
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
import {MatDialog} from '@angular/material/dialog';
import {TipOfTheDayDialogComponent} from '../tip-of-the-day/tip-of-the-day.component';
import {distinctUntilChanged, map, Subscription, switchMap, tap} from 'rxjs';

@Component({
  selector: 'app-tree.component',
  imports: [
    FormsModule
  ],
  templateUrl: './tree.component.html',
  styleUrl: './tree.component.css',
})
export class TreeComponent implements OnInit, OnDestroy {

  public rootData = inject(RootDataKeeperService);
  private _networkService = inject(NetworkService);
  private _activatedRoute = inject(ActivatedRoute);
  private _router = inject(Router);
  private _copyToClipboardService = inject(CopyToClipboardService);
  public favoritesService = inject(FavoritesService);
  private _dialog = inject(MatDialog);
  private _queryParamMapIdSubscription: Subscription | null = null;
  private _queryParamMapTipIdSubscription: Subscription | null = null;

  tree = signal<Tree | null>(null);
  latinMode: LatinModeEnum = LatinModeEnum.TranslatedOnly;
  LATIN_MODE_ENUM = LatinModeEnum;

  ngOnInit(): void {
    this._subscribeQueryParamMapId();
    this._subscribeQueryParamMapTipId()
  }

  private _subscribeQueryParamMapId() {
    this._queryParamMapIdSubscription = this._activatedRoute.queryParamMap
      .pipe(
        map(
          paramMap => paramMap.has("id") && paramMap.get("id") != null
            ? +(paramMap.get("id")!)
            : null
        ),
        distinctUntilChanged(),
        tap({
          next: id => {
            this.rootData.lastTreeId = id;
            console.log("queryParamMap changed: id:", id);  // TODO
          }
        }),
        switchMap(id => !!id
          ? this._networkService.getTreeById(id)
          : this._networkService.getTreeDefault()
        )
      )
      .subscribe({
        next: (data) => {
          this.tree.set(data);
        }, error: () => {
          alert(this.rootData.translationRoot()?.translations.network_error || NETWORK_ERROR_DEFAULT_MESSAGE);
        }
      });
  }

  private _subscribeQueryParamMapTipId() {
    this._queryParamMapTipIdSubscription = this._activatedRoute.queryParamMap
      .pipe(
        map(
          paramMap => paramMap.has("tipId") && paramMap.get("tipId") != null
            ? +(paramMap.get("tipId")!)
            : null
        ),
        distinctUntilChanged(),
        tap({
          next: tipId => {
            this.rootData.lastTipId = tipId;
            console.log("queryParamMap changed: tipId:", tipId);  // TODO
          }
        })
      )
      .subscribe({
        next: tipId => {
          this._dialog.closeAll();
          this._dialog.open(TipOfTheDayDialogComponent, {
            data: {tipId: tipId}
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
    const id = item.is_selected
      ? item.parent_id
      : item.id;
    if (!id) {
      this._router.navigate(['tree']);
    } else {
      this._router.navigate(
        ['tree'],
        {
          queryParams: {id},
          queryParamsHandling: "merge"
        }
      );
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
    const langKey = this.tree()?._language_key;
    return !!langKey && langKey in item.titles_by_languages;
  }

  onReadWikiClick(item: Item): void {
    const langKey = this.tree()?._language_key;
    if (!langKey || !(langKey in item.titles_by_languages)) {
      return;
    }
    const url = 'https://' + langKey + '.ruwiki.ru/wiki/' + item.titles_by_languages[langKey];  // TODO ruwiki
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

  onTipClick(): void {
    const tipId = this._activatedRoute.snapshot.queryParamMap.get("tipId");
    console.log("onTipClick(): tipId:", tipId);  // TODO
    this._dialog.closeAll();
    this._dialog.open(TipOfTheDayDialogComponent, {
      data: {tipId: tipId}
    });
  }

  ngOnDestroy() {
    this._queryParamMapIdSubscription?.unsubscribe();
    this._queryParamMapTipIdSubscription?.unsubscribe();
  }
}
