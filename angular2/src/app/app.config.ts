import {ApplicationConfig, importProvidersFrom, provideBrowserGlobalErrorListeners} from '@angular/core';
import {provideRouter} from '@angular/router';

import {routes} from './app.routes';
import {CookieModule} from 'ngx-cookie';
import {MatProgressSpinnerModule} from '@angular/material/progress-spinner';

export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    provideRouter(routes),
    importProvidersFrom(CookieModule.withOptions(), MatProgressSpinnerModule),
  ]
};
