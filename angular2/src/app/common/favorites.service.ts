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
  items = signal<FavoritesItem[]>([]);
  isFavoritesOpen = signal(false);

  constructor() {
    this.loadData();
  }

  private loadData(): void {
    const favorites = this._cookieService.getObject(this.favoritesCookieKey);
    this.items.set(favorites as FavoritesItem[] ?? []);
    this.isFavoritesOpen.set(!!favorites);
    this._hasCookiePrivate = !!favorites;
  }

  hasCookie(): boolean {
    return this._hasCookiePrivate;
  }

  addItem(level: Level, item: Item): void {
    const itemsClone = [...this.items()];
    itemsClone.push({
      id: item.id,
      rank_for_language: level.title_on_language,
      title_for_language: item.title_for_language,
      image_url: item.image_url,
      leaves_count: item.leaves_count
    } as FavoritesItem)
    this.items.set(itemsClone)
    this._cookieService.putObject(this.favoritesCookieKey, itemsClone, {expires: '2999-12-31'});
    this._hasCookiePrivate = true;
    this.isFavoritesOpen.set(true);
  }

  deleteItem(idToDelete: number): void {
    let itemsClone = [...this.items()];
    itemsClone = itemsClone.filter(item => item.id !== idToDelete);
    this.items.set(itemsClone);
    this._cookieService.putObject(this.favoritesCookieKey, itemsClone, {expires: '2999-12-31'});
  }

  isItemInFavorites(itemToCheck: Item): boolean {
    return this.items().some(item => item.id === itemToCheck.id);
  }
}
