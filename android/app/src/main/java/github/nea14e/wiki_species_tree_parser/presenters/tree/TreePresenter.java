package github.nea14e.wiki_species_tree_parser.presenters.tree;

import androidx.annotation.NonNull;

import java.util.List;

import github.nea14e.wiki_species_tree_parser.entities.Item;
import github.nea14e.wiki_species_tree_parser.entities.Level;
import github.nea14e.wiki_species_tree_parser.presenters.tree.view_entities.BaseTreeViewLevel;

public interface TreePresenter {
    void onItemExpandCollapseClicked(@NonNull Level curLevel, @NonNull Item curItem);

    interface Callback {
        void onNewTree(List<BaseTreeViewLevel> viewLevels);
    }
}
