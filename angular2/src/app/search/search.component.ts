import {Component, computed, inject, OnInit, signal} from '@angular/core';
import {SearchItem} from '../models/search-item';
import {RootDataKeeperService} from '../common/root-data-keeper.service';
import {NetworkService} from '../network.service';
import {ActivatedRoute, Router} from '@angular/router';
import {CopyToClipboardService} from '../common/copy-to-clipboard.service';
import {debounceTime, distinctUntilChanged, Subject} from 'rxjs';
import {Location} from "@angular/common";
import {FormsModule} from "@angular/forms";
import {MatProgressSpinner} from "@angular/material/progress-spinner";

@Component({
    selector: 'app-search.component',
    imports: [
        FormsModule,
      MatProgressSpinner,
    ],
    templateUrl: './search.component.html',
    styleUrl: './search.component.css',
})
export class SearchComponent implements OnInit {

  readonly ITEMS_COUNT_BY_QUERY = 2;  // TODO

  query = signal('');
    minQueryLength = 3;
  attachToTipId = signal<number | null>(null);
    queryChanged: Subject<string> = new Subject<string>();
  resultItems = signal<SearchItem[]>([]);
  isLoading = signal(false);
  isMore = signal(false);
  isResultsEmpty = computed(() =>
    !this.resultItems().length && this.query().length >= this.minQueryLength && !this.isLoading()
  );

    rootData = inject(RootDataKeeperService);
    private networkService = inject(NetworkService);
    private activatedRoute = inject(ActivatedRoute);
    private router = inject(Router);
    private location = inject(Location);
    private copyToClipboardService = inject(CopyToClipboardService);

    ngOnInit(): void {
        this.queryChanged  // see https://stackoverflow.com/a/52977862/7573844
            .pipe(
                debounceTime(1000), // wait 1 sec after the last event before emitting last event
                distinctUntilChanged() // only emit if value is different from previous value
            )
            .subscribe(data => {
                console.log('search:', data);
                // Call your function which calls API or do anything you would like do after a lag of 1 sec
                // noinspection JSIgnoredPromiseFromCall
                this.router.navigate(
                    ['search'],
                    {
                        queryParams: {q: data},
                        replaceUrl: true,
                        queryParamsHandling: 'merge'
                    }
                );
            });

        this.activatedRoute.queryParams.subscribe(params => {
            this.rootData.lastSearchParams = params;
          const q = params['q'] as string || '';
          this.query.set(q);
          const attachToTipId = !!params['attachToTipId']
            ? +params['attachToTipId']
            : null;
          this.attachToTipId.set(attachToTipId);
            this.runSearch(0);
        });
    }

    runSearch(offset: number): void {
      if (this.query().length < this.minQueryLength) {
        this.resultItems.set([]);
        this.isMore.set(false);
            return;
        }

      this.isLoading.set(true);
      this.networkService.search(this.query(), this.ITEMS_COUNT_BY_QUERY, offset)
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
              const prevResult = this.resultItems();
              prevResult.push(...result);
              this.resultItems.set(prevResult);
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
        this.router.navigate(['tree'], {queryParams: {id: item.id}});
    }

    onShareClick(): void {
        const val = window.location.href;
        this.copyToClipboardService.copy(val);
        alert(this.rootData.translationRoot()?.translations.link_copied);
    }

    onQueryInputChanged(inputText: string): void {
      this.query.set(inputText);
        this.queryChanged.next(inputText);
    }

    attachToTree(item: SearchItem): void {
        this.router.navigate(['admin/tip-translation'],
          {queryParams: {speciesPageUrl: item.page_url, tipId: this.attachToTipId()}}
        );
    }

    goBack(): void {
        this.location.back();
    }

    loadMore(): void {
      const newOffset = this.resultItems().length;
        this.runSearch(newOffset);
    }
}
