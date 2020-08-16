package github.nea14e.wiki_species_tree_parser;

import android.app.Application;

import github.nea14e.wiki_species_tree_parser.dagger.app.AppComponent;
import github.nea14e.wiki_species_tree_parser.dagger.app.DaggerAppComponent;

public class App extends Application {

    private static AppComponent appComponent;

    public static AppComponent getAppComponent() {
        if (appComponent == null) {
            appComponent = DaggerAppComponent.create();
        }
        return appComponent;
    }
}
