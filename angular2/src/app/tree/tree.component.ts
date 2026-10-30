import {
  Component,
  computed,
  ElementRef,
  HostListener,
  inject,
  OnDestroy,
  OnInit,
  signal,
  ViewChild
} from '@angular/core';
import {Tree} from '../models/tree';
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
import {distinctUntilChanged, filter, map, Subscription, switchMap, tap} from 'rxjs';
import {NgClass} from '@angular/common';
import {TreeHistoryItem} from '../models/tree-history-item';
import {PlainListItemComponent} from '../common/plain-list-item/plain-list-item';
import {FavoritesComponent} from '../favorites/favorites.component';
import {SearchMediatorService} from '../search/search-mediator.service';
import {SearchComponent} from '../search/search.component';

@Component({
  selector: 'app-tree.component',
  imports: [
    FormsModule,
    NgClass,
    PlainListItemComponent,
    FavoritesComponent,
    SearchComponent
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

  tree = signal<Tree | null>(null);
  selectedItemInfo = computed(() => this.tree()?.levels
    .map(level => {
      return {level, item: level.items.find(item => item.is_selected)}
    })
    .find(pair => !!pair.item)
  );
  @ViewChild("treeRoot") treeRootElement!: ElementRef;

  isShowSearch = signal(false);
  @ViewChild("searchQueryInput") searchQueryInput!: ElementRef;
  searchMediatorService = inject(SearchMediatorService);
  attachToTipId = signal<number | null>(null);
  private _attachToTipIdSubscription: Subscription | null = null;

  _backTreeHistory = signal<TreeHistoryItem[]>([]);
  _backTreeReversedHistory = computed(() => {
    const result = [];
    for (let i = this._backTreeHistory().length - 1; i >= 0; i--) {
      const item = this._backTreeHistory()[i];
      result.push(item);
    }
    return result;
  });
  _forwardTreeHistory = signal<TreeHistoryItem[]>([]);
  isBackEnabled = computed(() => this._backTreeHistory().length > 0);
  isForwardEnabled = computed(() => this._forwardTreeHistory().length > 0);
  isShowBackMenu = signal(false);
  isShowForwardMenu = signal(false);

  ngOnInit(): void {
    this._subscribeQueryParamMapId();
    this.openTipDialog();
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
          ? this._networkService.getTreeById
          (
            id,
            this.rootData.selectedLanguageKey1(),
            this.rootData.selectedLanguageKey2()
          )
          : this._networkService.getTreeDefault
          (
            this.rootData.selectedLanguageKey1(),
            this.rootData.selectedLanguageKey2()
          )
        )
      )
      .subscribe({
        next: (data) => {
          this.tree.set(data);
          this._goToSelectedItem();
        }, error: () => {
          alert(this.rootData.translationRoot()?.translations.network_error || NETWORK_ERROR_DEFAULT_MESSAGE);
        }
      });

    this._attachToTipIdSubscription = this._activatedRoute.queryParamMap
      .pipe(
        map(
          paramMap => paramMap.has("attachToTipId") && paramMap.get("attachToTipId") != null
            ? +(paramMap.get("attachToTipId")!)
            : null
        ),
        filter(attachToTipId => !!attachToTipId),
        distinctUntilChanged()
      )
      .subscribe(attachToTipId => {
        this.attachToTipId.set(attachToTipId);
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
    if (!this.tree()) {
      return;
    }

    this._backTreeHistory.update(prevHistory => {
      return [
        ...prevHistory,
        new TreeHistoryItem(
          this.selectedItemInfo()?.level ?? null,
          this.selectedItemInfo()?.item ?? null
        )
      ];
    });
    this._forwardTreeHistory.set([]);

    const id = item.is_selected
      ? item.parent_id
      : item.id;
    this._selectItemById(id);
  }

  _selectItemById(id: number | null): void {
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
    return !!item.title_for_language1;
  }

  onReadWikiClick(item: Item): void {
    const langKey = this.tree()?._language_key1;
    if (!langKey) {
      return;
    }
    const url = 'https://' + langKey + '.wikipedia.org/wiki/' + item.title_for_language1;
    window.open(url, '_blank');
  }

  onYandexItemClick(item: Item): void {
    const url = 'https://yandex.ru/search/?text=' + encodeURIComponent(item.title_for_language1);
    window.open(url, '_blank');
  }

  onShareItemClick(_: Item): void {
    const val = window.location.href;
    this._copyToClipboardService.copy(val);
    alert(this.rootData.translationRoot()?.translations.link_copied);
  }

  onToTreeRootClick(): void {
    if (!this.selectedItemInfo()) {
      return;
    }

    this._backTreeHistory.update(prevHistory => {
      return [
        ...prevHistory,
        new TreeHistoryItem(
          this.selectedItemInfo()?.level ?? null,
          this.selectedItemInfo()?.item ?? null
        )
      ];
    });
    this._forwardTreeHistory.set([]);

    this._selectItemById(null);
  }

  onFavoritesItemClick(level: Level, item: Item): void {
    if (!this.favoritesService.hasCookie()) {
      if (!confirm(this.rootData.translationRoot()?.translations.favorites_use_cookies_question)) {
        return;
      }
    }
    this.favoritesService.addItem(level, item);
  }

  onUnFavoritesItemClick(item: Item): void {
    if (!confirm(this.rootData.translationRoot()?.translations.delete_favorite_question)) {
      return;
    }
    this.favoritesService.deleteItem(item.id);
  }

  openTipDialog(): void {
    const tipIdString = this._activatedRoute.snapshot.queryParamMap.get("tipId");
    const tipId = !!tipIdString ? +tipIdString : null;
    console.log("openTipDialog(): tipId:", tipId);  // TODO
    this._dialog.closeAll();
    const matDialogRef = this._dialog.open(TipOfTheDayDialogComponent, {
      panelClass: 'customized-panel-dialog'
    });
    matDialogRef.componentInstance.loadTip(tipId);
  }

  ngOnDestroy() {
    this._queryParamMapIdSubscription?.unsubscribe();
    this._attachToTipIdSubscription?.unsubscribe();
  }

  cancelAttachingToTipId() {
    this._router.navigate(
      ['tree'],
      {
        queryParams: {attachToTipId: null},
        queryParamsHandling: "merge"
      }
    );
  }

  onSearchQueryChanged(value: string) {
    this.isShowSearch.set(true);
    this.isShowBackMenu.set(false);
    this.isShowForwardMenu.set(false);
    this.favoritesService.isFavoritesOpen.set(false);
    this.searchMediatorService.searchQuery.next(value);
  }

  onBackButtonClick() {
    this.isShowSearch.set(false);
    this.isShowBackMenu.update(value => !value);
    this.isShowForwardMenu.set(false);
    this.favoritesService.isFavoritesOpen.set(false);
  }

  onForwardButtonClick() {
    this.isShowSearch.set(false);
    this.isShowBackMenu.set(false);
    this.isShowForwardMenu.update(value => !value);
    this.favoritesService.isFavoritesOpen.set(false);
  }

  @HostListener('document:click', ['$event'])
  onDocumentClick(event: Event): void {
    const target = event.target as HTMLElement;
    if (!target.closest('.position-relative')) {
      this.isShowBackMenu.set(false);
      this.isShowForwardMenu.set(false);
      this.favoritesService.isFavoritesOpen.set(false);
      this.isShowSearch.set(false);
    }
  }

  onBackHistoryItemClick(selectedItem: TreeHistoryItem): void {
    this.isShowBackMenu.set(false);
    this.isShowForwardMenu.set(false);
    this.isShowSearch.set(false);

    const indexToMove = this._backTreeHistory()
      .findIndex(item => item.random_id === selectedItem.random_id);
    const backHistory = [...this._backTreeHistory()];
    const itemsToMove = backHistory.splice(indexToMove);
    this._backTreeHistory.set(backHistory);
    itemsToMove.splice(0, 1);

    this._forwardTreeHistory.set([
      ...itemsToMove,
      new TreeHistoryItem(
        this.selectedItemInfo()?.level ?? null,
        this.selectedItemInfo()?.item ?? null
      ),
      ...this._forwardTreeHistory()
    ])

    this._selectItemById(selectedItem.item?.id ?? null);
  }

  onForwardHistoryItemClick(selectedItem: TreeHistoryItem) {
    this.isShowBackMenu.set(false);
    this.isShowForwardMenu.set(false);
    this.isShowSearch.set(false);

    const indexToMove = this._forwardTreeHistory()
      .findIndex(item => item.random_id === selectedItem.random_id);
    const forwardHistory = [...this._forwardTreeHistory()];
    const itemsToMove = forwardHistory.splice(0, indexToMove + 1);
    this._forwardTreeHistory.set(forwardHistory);
    itemsToMove.splice(indexToMove, 1);

    this._backTreeHistory.set([
      ...this._backTreeHistory(),
      new TreeHistoryItem(
        this.selectedItemInfo()?.level ?? null,
        this.selectedItemInfo()?.item ?? null
      ),
      ...itemsToMove
    ]);

    this._selectItemById(selectedItem.item?.id ?? null);
  }

  onGoToSelectedItemClick() {
    this._goToSelectedItem();
  }

  private _goToSelectedItem(): void {
    requestAnimationFrame(() => {
      const selectedElement = document.querySelector('.item.selected');
      if (!!selectedElement) {
        selectedElement.scrollIntoView({behavior: 'smooth', block: 'center'});
      } else {
        this.treeRootElement.nativeElement.scrollIntoView({behavior: 'smooth', block: 'center'});
      }
    });
  }

  onFavoritesToggleClick() {
    this.favoritesService.isFavoritesOpen.update(value => !value);
    this.isShowBackMenu.set(false);
    this.isShowForwardMenu.set(false);
    this.isShowSearch.set(false);
  }

  onSearchQueryInputFocus() {
    this.favoritesService.isFavoritesOpen.set(false);
    this.isShowBackMenu.set(false);
    this.isShowForwardMenu.set(false);
    this.isShowSearch.set(true);
    setTimeout(() => {
      this.searchQueryInput.nativeElement.select();
    }, 0);
  }

  onSearchItemClick(itemId: number) {
    this.isShowSearch.set(false);
    this.searchQueryInput.nativeElement.blur();

    this._backTreeHistory.update(prevHistory => {
      return [
        ...prevHistory,
        new TreeHistoryItem(
          this.selectedItemInfo()?.level ?? null,
          this.selectedItemInfo()?.item ?? null
        )
      ];
    });
    this._forwardTreeHistory.set([]);

    this._selectItemById(itemId);
  }
}
