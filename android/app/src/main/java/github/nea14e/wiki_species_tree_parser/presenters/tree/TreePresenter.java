package github.nea14e.wiki_species_tree_parser.presenters.tree;

import java.util.List;

import github.nea14e.wiki_species_tree_parser.presenters.tree.view_entities.BaseTreeViewLevel;

public interface TreePresenter {
    void onCreateView();

    void onItemExpandCollapseClicked(long itemId);

    interface Callback {
        void onNewTree(List<BaseTreeViewLevel> viewLevels);
    }
}
