import {Injectable} from '@angular/core';
import {FavoritesItem, Item} from './models';
import {NetworkService} from './network.service';
import {CookieService} from 'ngx-cookie';

@Injectable({
  providedIn: 'root'
})
export class FavoritesService {

  private ids: number[];
  private hasCookiePrivate: boolean;
  public items: FavoritesItem[] | null;
  isFavoritesOpen = false;

  constructor(private cookieService: CookieService,
              private networkService: NetworkService) {
    this.loadData();
  }

  private loadData(): void {
    const favorites = this.cookieService.getObject('favorites');
    if (!!favorites) {
      this.ids = favorites as number[];
      this.hasCookiePrivate = true;
    } else {
      this.ids = [];
      this.hasCookiePrivate = false;
    }

    this.networkService.getFavorites(this.ids)
      .subscribe(data => {
        this.items = data;
      });
  }

  hasCookie(): boolean {
    return this.hasCookiePrivate;
  }

  addItem(item: Item): void {
    this.ids.push(item.id);
    this.cookieService.putObject('favorites', this.ids);
    console.log('Add:', this.ids);  // TODO for debug
    this.hasCookiePrivate = true;
    this.loadData();
    this.isFavoritesOpen = true;
  }

  toggleTab(): void {
    this.isFavoritesOpen = !(this.isFavoritesOpen);
  }
}
