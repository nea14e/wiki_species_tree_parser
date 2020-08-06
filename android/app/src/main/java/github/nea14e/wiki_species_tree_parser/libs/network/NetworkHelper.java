package github.nea14e.wiki_species_tree_parser.libs.network;

import java.util.List;

import github.nea14e.wiki_species_tree_parser.models.Check;
import github.nea14e.wiki_species_tree_parser.models.Level;
import github.nea14e.wiki_species_tree_parser.models.SearchItem;
import github.nea14e.wiki_species_tree_parser.models.TipOfTheDay;
import github.nea14e.wiki_species_tree_parser.models.Tree;
import github.nea14e.wiki_species_tree_parser.libs.network.retrofit.SmartCallback;

public interface NetworkHelper {
    void getChildesById(Long id, SmartCallback<List<Level>> callback);

    void getTreeById(Long id, SmartCallback<Tree> callback);

    void getTreeDefault(SmartCallback<Tree> callback);

    void searchByWords(String words, int offset, SmartCallback<List<SearchItem>> callback);

    void getTipOfTheDay(SmartCallback<TipOfTheDay> callback);

    void check(SmartCallback<Check> callback);
}
