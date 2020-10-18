import { Component, OnInit } from '@angular/core';
import {Item, Level, Tree} from '../models';
import {ActivatedRoute, Router} from '@angular/router';
import {NetworkService} from '../network.service';
import {RootDataKeeperService} from '../root-data-keeper.service';

@Component({
  selector: 'app-tree',
  templateUrl: './tree.component.html',
  styleUrls: [
    '../app.component.css',
    './tree.component.css'
  ]
})
export class TreeComponent implements OnInit {

  tree: Tree;

  constructor(public rootData: RootDataKeeperService,
              private networkService: NetworkService,
              private activatedRoute: ActivatedRoute,
              private router: Router) { }

  ngOnInit(): void {
    this.activatedRoute.queryParams.subscribe(params => {
        const id: number = +params.id || null;
        if (!id) {
          this.networkService.getTreeDefault().subscribe(data => {
            this.tree = data;
          }, error => {
            alert(error);
          });
        } else {
          this.networkService.getTreeById(id).subscribe(data => {
            this.tree = data;
          }, error => {
            alert(error);
          });
        }
      });
  }

  // noinspection JSMethodCanBeStatic
  getItemClass(item: Item): string {
    if (item.is_selected === true) {
      return 'selected';
    } else if (item.is_expanded === true) {
      return 'expanded';
    }
    return '';
  }

  onItemClick(item: Item): void {
    let id: number;
    if (item.is_selected) {
      id = item.parent_id;
    } else {
      id = item.id;
    }
    if (!id) {
      this.router.navigate(['tree']);
    } else {
      this.router.navigate(['tree'], { queryParams: { id } });
    }
  }

  // noinspection JSMethodCanBeStatic
  getLevelClass(level: Level): string {
    if (level.is_level_has_selected_item) {
      return 'has-selected';
    }
    return '';
  }

  readItemOnWiki(item: Item): void {
    const url = 'https://' + this.tree._language_key + '.wikipedia.org/wiki/' + item.wiki_url_for_language;
    window.open(url, '_blank');
  }

  googleItem(item: Item): void {
    const url = 'https://www.google.com/search?q=' + encodeURIComponent(item.title_for_language);
    window.open(url, '_blank');
  }

}
