import {Component, OnInit} from '@angular/core';
import {NetworkService} from './network.service';
import {Item, Level, TranslationRoot, Tree} from './models';
import {ActivatedRoute, Router} from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {

  translationRoot: TranslationRoot;

  constructor(private networkService: NetworkService,
              private activatedRoute: ActivatedRoute,
              private router: Router) {}

  ngOnInit(): void {
    this.networkService.getTranslations().subscribe(data => {
      this.translationRoot = data;
    }, error => {
      alert(error);
    });
  }
}
