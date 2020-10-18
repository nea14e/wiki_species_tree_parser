import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import {HttpClientModule} from '@angular/common/http';
import {RouterModule, Routes} from '@angular/router';
import { TreeComponent } from './tree/tree.component';
import { TipOfTheDayComponent } from './tip-of-the-day/tip-of-the-day.component';

const routes: Routes = [
  { path: 'tip', component: TipOfTheDayComponent },
  { path: 'tree', component: TreeComponent },
  { path: '**', redirectTo: 'tip' },
];

@NgModule({
  declarations: [
    AppComponent,
    TipOfTheDayComponent,
    TreeComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    RouterModule.forRoot(routes)
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
