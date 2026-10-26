import {Component, computed, inject} from '@angular/core';
import {FavoritesItem} from '../models/favorites-item';
import {RootDataKeeperService} from '../common/root-data-keeper.service';
import {FavoritesService} from '../common/favorites.service';
import {Router} from '@angular/router';

@Component({
  selector: 'app-favorites',
  imports: [],
  templateUrl: './favorites.component.html',
  styleUrl: './favorites.component.css',
})
export class FavoritesComponent {

  rootData = inject(RootDataKeeperService);
  favoritesService = inject(FavoritesService);
  private _router = inject(Router)

  isFavoritesEmpty = computed(
    () => !this.favoritesService.items() || this.favoritesService.items().length === 0
  );

  onDeleteItemClick(item: FavoritesItem): void {
    this.favoritesService.deleteItem(item.id);
  }

  toTree(id: number): void {
    this.favoritesService.isFavoritesOpen.set(false);
    this._router.navigate(['tree'], {queryParams: {id}});
  }
}
