import { Component, OnInit } from '@angular/core';
import {RootDataKeeperService} from '../root-data-keeper.service';
import {FavoritesItem} from '../models';
import {NetworkService} from '../network.service';
import {FavoritesService} from '../favorites.service';

@Component({
  selector: 'app-favorites',
  templateUrl: './favorites.component.html',
  styleUrls: ['./favorites.component.css', '../app.component.css']
})
export class FavoritesComponent implements OnInit {
  items: FavoritesItem[] = [];

  constructor(public rootData: RootDataKeeperService,
              private networkService: NetworkService,
              public favoritesService: FavoritesService
              ) { }

  ngOnInit(): void {
  }

  onDeleteItemClick(item: FavoritesItem): void {
    this.favoritesService.deleteItem(item);
  }
}
