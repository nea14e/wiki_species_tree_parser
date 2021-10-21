import { Component, OnInit } from '@angular/core';
import {RootDataKeeperService} from '../root-data-keeper.service';

@Component({
  selector: 'app-favorites',
  templateUrl: './favorites.component.html',
  styleUrls: ['./favorites.component.css', '../app.component.css']
})
export class FavoritesComponent implements OnInit {

  constructor(public rootData: RootDataKeeperService) { }

  ngOnInit(): void {
  }

}
