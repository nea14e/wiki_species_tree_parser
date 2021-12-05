import { Component, OnInit } from '@angular/core';
import {RootDataKeeperService} from '../root-data-keeper.service';
import {FavoritesItem} from '../models';
import {NetworkService} from '../network.service';
import {FavoritesService} from '../favorites.service';
import {Router} from '@angular/router';

@Component({
  selector: 'app-favorites',
  templateUrl: './favorites.component.html',
  styleUrls: ['./favorites.component.css', '../app.component.css']
})
export class FavoritesComponent implements OnInit {
  items: FavoritesItem[] = [];

  constructor(public rootData: RootDataKeeperService,
              private networkService: NetworkService,
              public favoritesService: FavoritesService,
              private router: Router
              ) { }

  ngOnInit(): void {
  }

  onDeleteItemClick(item: FavoritesItem): void {
    this.favoritesService.deleteItem(item.id);
  }

  toTree(id: number): void {
      this.router.navigate(['tree'], {queryParams: { id } });
  }
}
