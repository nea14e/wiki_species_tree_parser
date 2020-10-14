import {Component, OnInit} from '@angular/core';
import {NetworkService} from './network.service';
import {Item, Level, Tree} from './models';

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
    this.updLevelSelected();
  }

  private updLevelSelected(): void {
    for (let level of this.tree.levels) {
      let isLevelHasItem = false;
      for (let item of level.items) {
        if (item.is_selected) {
          isLevelHasItem = true;
          level.is_level_has_selected_item = true;
        }
      }
      if (!isLevelHasItem) {
        level.is_level_has_selected_item = false;
      }
    }
  }

  getLevelClass(level: Level): string {
    if (level.is_level_has_selected_item) {
      return 'has-selected';
    }
    return '';
  }

  readItemOnWiki(item: Item) {
    const url = 'https://' + this.tree._language_key + '.wikipedia.org/wiki/' + item.wiki_url_for_language;
    window.open(url, '_blank');
  }

  googleItem(item: Item) {
    const url = 'https://www.google.com/search?q=' + encodeURIComponent(item.title_for_language);
    window.open(url, '_blank');
  }
}
