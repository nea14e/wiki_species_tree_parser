import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import {HttpClientModule} from '@angular/common/http';
import {RouterModule, Routes} from '@angular/router';
import { TreeComponent } from './tree/tree.component';
import { TipOfTheDayComponent } from './tip-of-the-day/tip-of-the-day.component';
import { AuthorsComponent } from './authors/authors.component';
import {FormsModule} from '@angular/forms';
import {CommonModule} from '@angular/common';

const routes: Routes = [
  { path: 'tip', component: TipOfTheDayComponent },
  { path: 'tree', component: TreeComponent },
  { path: 'authors', component: AuthorsComponent },
  { path: '**', redirectTo: 'tip' },
];

@NgModule({
  declarations: [
    AppComponent,
    TipOfTheDayComponent,
    TreeComponent,
    AuthorsComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    RouterModule.forRoot(routes),
    CommonModule,
    FormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
