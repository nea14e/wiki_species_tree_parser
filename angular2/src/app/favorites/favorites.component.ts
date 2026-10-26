import {Component, computed, inject, signal} from '@angular/core';
import {FavoritesItem} from '../models/favorites-item';
import {RootDataKeeperService} from '../common/root-data-keeper.service';
import {FavoritesService} from '../common/favorites.service';
import {Router} from '@angular/router';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';

@Component({
  selector: 'app-favorites',
  imports: [
    ReactiveFormsModule,
    FormsModule
  ],
  templateUrl: './favorites.component.html',
  styleUrl: './favorites.component.css',
})
export class FavoritesComponent {

  rootData = inject(RootDataKeeperService);
  favoritesService = inject(FavoritesService);
  private _router = inject(Router)

  filterText = signal("");
  filteredItems = computed(
    () => !!this.filterText()
      ? this.favoritesService.items().filter(item => item.title_for_language.toUpperCase().includes(this.filterText().toUpperCase()))
      : this.favoritesService.items()
  );
  isFavoritesEmpty = computed(
    () => !this.favoritesService.items() || this.favoritesService.items().length === 0
  );

  onFilterTextChanged(filterText: string) {
    this.filterText.set(filterText);
  }

  onDeleteItemClick(item: FavoritesItem): void {
    if (!confirm(this.rootData.translationRoot()?.translations.delete_favorite_question)) {
      return;
    }
    this.favoritesService.deleteItem(item.id);
  }

  toTree(id: number): void {
    this.favoritesService.isFavoritesOpen.set(false);
    this._router.navigate(['tree'], {queryParams: {id}});
  }
}
