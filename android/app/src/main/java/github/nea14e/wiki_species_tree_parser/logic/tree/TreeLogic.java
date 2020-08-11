package github.nea14e.wiki_species_tree_parser.logic.tree;

import androidx.annotation.NonNull;

import github.nea14e.wiki_species_tree_parser.entities.Item;
import github.nea14e.wiki_species_tree_parser.entities.Level;
import github.nea14e.wiki_species_tree_parser.entities.Tree;

public interface TreeLogic {
    void expandOrCollapse(@NonNull Level curLevel, @NonNull Item curItem);

    interface Callback {
        void onNewTree(Tree tree);
    }
}
