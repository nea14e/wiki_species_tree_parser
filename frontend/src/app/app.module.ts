import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { CookieModule } from 'ngx-cookie';

import { AppComponent } from './app.component';
import {HttpClientModule} from '@angular/common/http';
import {RouterModule, Routes} from '@angular/router';
import { TreeComponent } from './tree/tree.component';
import { TipOfTheDayComponent } from './tip-of-the-day/tip-of-the-day.component';
import { AuthorsComponent } from './authors/authors.component';
import {FormsModule} from '@angular/forms';
import {CommonModule} from '@angular/common';
import { SearchComponent } from './search/search.component';
import { DbTasksComponent } from './admin/db-tasks/db-tasks.component';
import { AdminUsersComponent } from './admin/admin-users/admin-users.component';
import { TipTranslationComponent } from './admin/tip-translation/tip-translation.component';

const routes: Routes = [
  { path: 'tip', component: TipOfTheDayComponent },
  { path: 'tree', component: TreeComponent },
  { path: 'search', component: SearchComponent },
  { path: 'authors', component: AuthorsComponent },
  { path: 'admin', redirectTo: 'tip' },
  { path: 'admin/db-tasks', component: DbTasksComponent },
  { path: 'admin/tip-translation', component: TipTranslationComponent },
  { path: 'admin/admin-users', component: AdminUsersComponent },
  { path: '**', redirectTo: 'tip' },
];

@NgModule({
  declarations: [
    AppComponent,
    TipOfTheDayComponent,
    TreeComponent,
    SearchComponent,
    AuthorsComponent,
    DbTasksComponent,
    AdminUsersComponent,
    TipTranslationComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    RouterModule.forRoot(routes),
    CommonModule,
    FormsModule,
    CookieModule.forRoot()
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
