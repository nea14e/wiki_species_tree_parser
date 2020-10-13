import {Component, OnInit} from '@angular/core';
import {NetworkService} from './network.service';
import {Item, Tree} from './models';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {

  tree: Tree;

  constructor(private networkService: NetworkService) {}

  ngOnInit(): void {
    this.networkService.getTreeDefault().subscribe(data => {
      this.tree = data;
    }, error => {
      alert(error);
    });
  }

  getItemClass(item: Item): string {
    if (item.is_selected === true) {
      return 'selected';
    } else if (item.is_expanded === true) {
      return 'expanded';
    }
    return '';
  }

  onItemClick(item: Item): void {
    if (item.is_expanded === false) {
      item.is_expanded = true;
    } else if (item.is_selected === false) {
      item.is_selected = true;
    } else {
      item.is_expanded = false;
      item.is_selected = false;
    }
  }

}
