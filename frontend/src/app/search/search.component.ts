import { Component, OnInit } from '@angular/core';
import {NetworkService} from '../network.service';
import {CopyToClipboardService} from '../copy-to-clipboard.service';
import {ActivatedRoute, Router} from '@angular/router';
import {RootDataKeeperService} from '../root-data-keeper.service';
import {SearchItem} from '../models';
import {Subject} from 'rxjs';
import {debounceTime, distinctUntilChanged, filter} from 'rxjs/internal/operators';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: [
    '../app.component.css',
    './search.component.css'
  ]
})
export class SearchComponent implements OnInit {

  query = '';
  queryChanged: Subject<string> = new Subject<string>();
  resultItems: SearchItem[] = [];

  constructor(public rootData: RootDataKeeperService,
              private networkService: NetworkService,
              private activatedRoute: ActivatedRoute,
              private router: Router,
              private copyToClipboardService: CopyToClipboardService) { }

  ngOnInit(): void {
    this.queryChanged  // see https://stackoverflow.com/a/52977862/7573844
      .pipe(
        debounceTime(1000), // wait 1 sec after the last event before emitting last event
        distinctUntilChanged() // only emit if value is different from previous value
      )
      .subscribe(data => {
        console.log('search:', data);
        // Call your function which calls API or do anything you would like do after a lag of 1 sec
        this.router.navigate(['search'], {queryParams: {q: data}, replaceUrl: true});
      });

    this.activatedRoute.queryParams.subscribe(params => {
      this.rootData.lastSearchParams = params;
      this.query = params.q || '';
      this.runSearch(0);
    });
  }

  runSearch(offset: number): void {
    if (this.query.length < 3) {
      this.resultItems = [];
      return;
    }

    this.networkService.search(this.query, offset)
      .subscribe(result => {
        console.log('result:', result);
        this.resultItems = result;
      }, () => {
        alert(this.rootData.translationRoot.translations.network_error);
      });
  }

  onItemClick(item: SearchItem): void {
    this.router.navigate(['tree'], {queryParams: {id: item.id}});
  }

  onShareClick(): void {
    const val = window.location.href;
    this.copyToClipboardService.copy(val);
    alert(this.rootData.translationRoot?.translations.link_copied);
  }

  onQueryInputChanged(inputText: string): void {
    this.queryChanged.next(inputText);
  }
}
