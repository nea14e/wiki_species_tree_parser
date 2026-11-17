import {inject, Service, signal} from '@angular/core';
import {CookieService} from 'ngx-cookie';
import {FavoritesItem} from '../models/favorites-item';
import {Item} from '../models/item';
import {Level} from '../models/level';

@Service()
export class FavoritesService {

  private readonly favoritesCookieKey = 'favoriteItems';
  private _cookieService = inject(CookieService);
  private _hasCookiePrivate = false;
  private _items = signal<FavoritesItem[]>([]);
  items = this._items.asReadonly();
  isFavoritesOpen = signal(false);

  constructor() {
    this.loadData();
  }

  private loadData(): void {
    const favorites = this._cookieService.getObject(this.favoritesCookieKey);
    this._items.set(favorites as FavoritesItem[] ?? []);
    this._hasCookiePrivate = !!favorites;
  }

  hasCookie(): boolean {
    return this._hasCookiePrivate;
  }

  addItem(level: Level, item: Item): void {
    const itemsClone = [...this._items()];
    itemsClone.push({
      id: item.id,
      rank_for_language1: level.rank_for_language1,
      rank_latin: level.rank_latin,
      title_for_language1: item.title_for_language1,
      title_for_language2: item.title_for_language2,
      title_latin: item.title_latin,
      image_url: item.image_url,
      leaves_count: item.leaves_count
    } as FavoritesItem)
    this._items.set(itemsClone)
    this._cookieService.putObject(this.favoritesCookieKey, itemsClone, {expires: '2999-12-31'});
    this._hasCookiePrivate = true;
    this.isFavoritesOpen.set(true);
  }

  deleteItem(idToDelete: number): void {
    let itemsClone = [...this._items()];
    itemsClone = itemsClone.filter(item => item.id !== idToDelete);
    this._items.set(itemsClone);
    this._cookieService.putObject(this.favoritesCookieKey, itemsClone, {expires: '2999-12-31'});
  }

  isItemInFavorites(itemToCheck: Item): boolean {
    return this._items().some(item => item.id === itemToCheck.id);
  }
}
