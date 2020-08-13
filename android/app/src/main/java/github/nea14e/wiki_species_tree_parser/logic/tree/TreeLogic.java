package github.nea14e.wiki_species_tree_parser.logic.tree;

import github.nea14e.wiki_species_tree_parser.entities.Tree;

public interface TreeLogic {
    void expandOrCollapse(long itemId);

    interface Callback {
        void onNewTree(Tree tree);
    }
}
