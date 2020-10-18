import { Component, OnInit } from '@angular/core';
import {Location} from '@angular/common';
import {RootDataKeeperService} from '../root-data-keeper.service';

@Component({
  selector: 'app-authors',
  templateUrl: './authors.component.html',
  styleUrls: [
    '../app.component.css',
    './authors.component.css'
  ]
})
export class AuthorsComponent implements OnInit {

  constructor(public rootData: RootDataKeeperService,
              private location: Location) { }

  ngOnInit(): void {
  }

  onBackClick(): void {
    this.location.back();
  }

}
