import {Service} from '@angular/core';
import {BehaviorSubject} from 'rxjs';

@Service()
export class SearchMediatorService {
  searchQuery = new BehaviorSubject<string>("");
}
