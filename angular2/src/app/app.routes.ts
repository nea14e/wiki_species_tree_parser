import {Routes} from '@angular/router';
import {TipOfTheDayComponent} from './tip-of-the-day/tip-of-the-day.component';
import {TreeComponent} from './tree/tree.component';

export const routes: Routes = [
  {path: 'tip', component: TipOfTheDayComponent},
  {path: 'tree', component: TreeComponent},
  // { path: 'search', component: SearchComponent },
  // { path: 'authors', component: AuthorsComponent },
  // { path: 'admin', redirectTo: 'tip' },
  // { path: 'admin/db-tasks', component: DbTasksComponent },
  // { path: 'admin/tip-translation', component: TipTranslationComponent },
  // { path: 'admin/filling-stats', component: FillingStatsComponent },
  // { path: 'admin/admin-users', component: AdminUsersComponent },
  {path: '**', redirectTo: 'tip'},
];
