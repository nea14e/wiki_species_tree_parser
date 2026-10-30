import {Component, computed, inject, input, OnDestroy, OnInit, output, signal} from '@angular/core';
import {SearchItem} from '../models/search-item';
import {RootDataKeeperService} from '../common/root-data-keeper.service';
import {NetworkService} from '../network.service';
import {Router} from '@angular/router';
import {debounceTime, distinctUntilChanged, Subscription, tap} from 'rxjs';
import {FormsModule} from "@angular/forms";
import {MatProgressSpinner} from "@angular/material/progress-spinner";
import {SearchMediatorService} from './search-mediator.service';

@Component({
  selector: 'app-search',
  imports: [
    FormsModule,
    MatProgressSpinner,
  ],
  templateUrl: './search.component.html',
  styleUrl: './search.component.css',
})
export class SearchComponent implements OnInit, OnDestroy {

  readonly MIN_QUERY_LENGTH = 3;
  readonly ITEMS_COUNT_BY_QUERY = 3;

  onSearchItemClick = output<number>();

  private _searchMediatorService = inject(SearchMediatorService);
  private _searchQuerySubscription: Subscription | null = null;
  searchQuery = signal("");
  resultItems = signal<SearchItem[]>([]);
  isLoading = signal(false);
  isMore = signal(false);
  isLoadingMore = signal(false);
  isResultsEmpty = computed(() =>
    !this.resultItems().length && this.searchQuery().length >= this.MIN_QUERY_LENGTH && !this.isLoading()
  );
  isQueryTooShort = computed(() =>
    this.searchQuery().length < this.MIN_QUERY_LENGTH && !this.isLoading()
  );

  attachToTipId = input<number | null>(null);

  rootData = inject(RootDataKeeperService);
  private networkService = inject(NetworkService);
  private router = inject(Router);

  ngOnInit(): void {
    this._searchQuerySubscription = this._searchMediatorService.searchQuery  // see https://stackoverflow.com/a/52977862/7573844
      .pipe(
        tap({
          next: value => {
            this.searchQuery.set(value);
          }
        }),
        debounceTime(1000), // wait 1 sec after the last event before emitting last event
        distinctUntilChanged() // only emit if value is different from previous value
      )
      .subscribe(data => {
        console.log('search:', data);
        this.runSearch(0);
      });
  }

  runSearch(offset: number): void {
    if (this.searchQuery().length < this.MIN_QUERY_LENGTH) {
      this.resultItems.set([]);
      this.isMore.set(false);
      this.isLoading.set(false);
      return;
    }

    this.isLoading.set(true);
    this.isLoadingMore.set(offset > 0);
    this.networkService.search
    (
      this.searchQuery(), this.ITEMS_COUNT_BY_QUERY, offset,
      this.rootData.selectedLanguageKey1(), this.rootData.selectedLanguageKey2()
    )
      .subscribe({
        next: result => {
          console.log('result:', result);
          const isMore = result.length > this.ITEMS_COUNT_BY_QUERY;
          this.isMore.set(isMore);
          if (this.isMore()) {
            result.splice(this.ITEMS_COUNT_BY_QUERY);
          }
          console.log('modified result:', result);
          if (offset > 0) {
            this.resultItems.set([
              ...this.resultItems(),
              ...result
            ]);
          } else {
            this.resultItems.set(result);
          }
          this.isLoading.set(false);
        }, error: () => {
          alert(this.rootData.translationRoot()?.translations.network_error);
          this.isLoading.set(false);
        }
      });
  }

  onItemClick(item: SearchItem): void {
    this.onSearchItemClick.emit(item.id);
  }

  attachToTree(item: SearchItem): void {
    this.router.navigate(['admin/tip-translation'],
      {queryParams: {speciesPageUrl: item.page_id, tipId: this.attachToTipId()}}
    );
  }

  loadMore(): void {
    const newOffset = this.resultItems().length;
    this.runSearch(newOffset);
  }

  ngOnDestroy() {
    this._searchQuerySubscription?.unsubscribe();
  }
}
