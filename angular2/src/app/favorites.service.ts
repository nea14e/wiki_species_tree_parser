import {inject, Service, signal} from '@angular/core';
import {NetworkService} from './network.service';
import {CookieService} from 'ngx-cookie';
import {FavoritesItem} from './models/favorites-item';
import {Item} from './models/item';

@Service()
export class FavoritesService {

  private _cookieService = inject(CookieService);
  private _networkService = inject(NetworkService);
  private _ids: number[] = [];
  private _hasCookiePrivate = false;
  items = signal<FavoritesItem[]>([]);
  isFavoritesOpen = signal(false);

  constructor() {
    this.loadData();
  }

  private loadData(): void {
    const favorites = this._cookieService.getObject('favorites');
    if (!!favorites) {
      this._ids = favorites as number[];
      this._hasCookiePrivate = true;
    } else {
      this._ids = [];
      this._hasCookiePrivate = false;
    }

    this._networkService.getFavorites(this._ids)
      .subscribe(data => {
        this.items.set(data);
      });
  }

  hasCookie(): boolean {
    return this._hasCookiePrivate;
  }

  addItem(item: Item): void {
    this._ids.push(item.id);
    this._cookieService.putObject('favorites', this._ids);
    console.log('Add:', this._ids);  // TODO for debug
    this._hasCookiePrivate = true;
    this.loadData();
    this.isFavoritesOpen.set(true);
  }

  deleteItem(itemId: number): void {
    this._ids = this._ids.filter(id => itemId !== id);
    this._cookieService.putObject('favorites', this._ids);
    console.log('Delete', itemId);  // TODO for debug
    this.loadData();
  }

  toggleTab(): void {
    this.isFavoritesOpen.update(prevValue => !prevValue);
  }

  isItemInFavorites(item: Item): boolean {
    return this._ids.includes(item.id);
  }
}
