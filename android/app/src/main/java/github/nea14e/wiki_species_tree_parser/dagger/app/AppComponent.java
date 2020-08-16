package github.nea14e.wiki_species_tree_parser.dagger.app;

import dagger.Component;
import github.nea14e.wiki_species_tree_parser.fragments.BaseFragment;
import github.nea14e.wiki_species_tree_parser.fragments.tip_of_the_day.TipOfTheDayFragment;
import github.nea14e.wiki_species_tree_parser.fragments.tree.level_items.ListItemViewHolder;
import github.nea14e.wiki_species_tree_parser.fragments.tree.levels.DetailedLevelViewHolder;
import github.nea14e.wiki_species_tree_parser.fragments.tree.levels.ShortenedLevelViewHolder;
import github.nea14e.wiki_species_tree_parser.logic.tree.OneSelectionTreeLogic;
import github.nea14e.wiki_species_tree_parser.logic.tree.SimpleReloadTreeLogic;

@AppScope
@Component(modules = {AppModule.class})
public interface AppComponent {
    void inject(BaseFragment baseFragment);
    void inject(TipOfTheDayFragment tipOfTheDayFragment);

    void inject(OneSelectionTreeLogic oneSelectionTreeLogic);
    void inject(SimpleReloadTreeLogic simpleReloadTreeLogic);

    void inject(ListItemViewHolder listItemViewHolder);

    void inject(DetailedLevelViewHolder detailedLevelViewHolder);

    void inject(ShortenedLevelViewHolder shortenedLevelViewHolder);
}
