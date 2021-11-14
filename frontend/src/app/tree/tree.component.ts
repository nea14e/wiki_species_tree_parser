import {Component, OnInit} from '@angular/core';
import {Item, LatinModeEnum, Level, Tree} from '../models';
import {ActivatedRoute, Router} from '@angular/router';
import {NetworkService} from '../network.service';
import {RootDataKeeperService} from '../root-data-keeper.service';
import {CopyToClipboardService} from '../copy-to-clipboard.service';
import {CookieService} from 'ngx-cookie';
import {FavoritesService} from "../favorites.service";

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
  latinMode: LatinModeEnum = LatinModeEnum.TranslatedOnly;
  LATIN_MODE_ENUM = LatinModeEnum;

  constructor(public rootData: RootDataKeeperService,
              private networkService: NetworkService,
              private activatedRoute: ActivatedRoute,
              private router: Router,
              private copyToClipboardService: CopyToClipboardService,
              public favoritesService: FavoritesService) { }

  ngOnInit(): void {
    this.activatedRoute.queryParams.subscribe(params => {
        this.rootData.lastTreeParams = params;
        const id: number = +params.id || null;
        if (!id) {
          this.networkService.getTreeDefault().subscribe(data => {
            this.tree = data;
          }, () => {
            alert(this.rootData.translationRoot.translations.network_error);
          });
        } else {
          this.networkService.getTreeById(id).subscribe(data => {
            this.tree = data;
          }, () => {
            alert(this.rootData.translationRoot.translations.network_error);
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

  onReadWikiClick(item: Item): void {
    const url = 'https://' + this.tree._language_key + '.wikipedia.org/wiki/' + item.wiki_url_for_language;
    window.open(url, '_blank');
  }

  onGoogleItemClick(item: Item): void {
    const url = 'https://www.google.com/search?q=' + encodeURIComponent(item.title_for_language);
    window.open(url, '_blank');
  }

  onShareItemClick(item: Item): void {
    const val = window.location.href;
    this.copyToClipboardService.copy(val);
    alert(this.rootData.translationRoot?.translations.link_copied);
  }

  onToTreeRootClick(): void {
    this.router.navigate(['tree']);
  }

  onFavoritesItemClick(item: Item): void {
    if (!this.favoritesService.hasCookie()) {
      if (!confirm(this.rootData.translationRoot?.translations.favorites_use_cookies_question)) {
        return;
      }
    }
    this.favoritesService.addItem(item);
  }

  onUnFavoritesItemClick(item: Item): void {
    this.favoritesService.deleteItem(item.id);
  }
}
