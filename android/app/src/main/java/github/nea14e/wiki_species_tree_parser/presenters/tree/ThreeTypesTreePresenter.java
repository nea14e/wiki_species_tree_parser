package github.nea14e.wiki_species_tree_parser.presenters.tree;

import androidx.annotation.Nullable;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

import github.nea14e.wiki_species_tree_parser.entities.Item;
import github.nea14e.wiki_species_tree_parser.entities.Level;
import github.nea14e.wiki_species_tree_parser.entities.Tree;
import github.nea14e.wiki_species_tree_parser.logic.tree.OneSelectionTreeLogic;
import github.nea14e.wiki_species_tree_parser.logic.tree.TreeLogic;
import github.nea14e.wiki_species_tree_parser.presenters.tree.view_entities.BaseTreeViewLevel;
import github.nea14e.wiki_species_tree_parser.presenters.tree.view_entities.DetailedTreeViewLevel;
import github.nea14e.wiki_species_tree_parser.presenters.tree.view_entities.ListItemsTreeViewLevel;
import github.nea14e.wiki_species_tree_parser.presenters.tree.view_entities.ShortenedTreeViewLevel;

public class ThreeTypesTreePresenter implements TreePresenter, TreeLogic.Callback {

    private final TreePresenter.Callback callback;
    private TreeLogic treeLogic = null;

    public ThreeTypesTreePresenter(@Nullable Long initId, TreePresenter.Callback callback) {
        this.callback = callback;
        treeLogic = new OneSelectionTreeLogic(initId, this);
    }

    @Override
    public void onItemExpandCollapseClicked(long itemId) {
        treeLogic.expandOrCollapse(itemId);
    }


    @Override
    public void onNewTree(Tree tree) {
        List<BaseTreeViewLevel> viewLevels;
        if (tree.id == null) {
            viewLevels = treeTransormPlain(tree);
        } else {
            viewLevels = treeTransormExpanded(tree);
        }
        callback.onNewTree(viewLevels);
    }


    private List<BaseTreeViewLevel> treeTransormPlain(Tree tree) {
        List<BaseTreeViewLevel> viewLevels = new ArrayList<>(tree.levels.size());
        for (Level level : tree.levels) {
            viewLevels.add(new ListItemsTreeViewLevel(level));
        }
        return viewLevels;
    }

    private List<BaseTreeViewLevel> treeTransormExpanded(Tree tree) {
        List<BaseTreeViewLevel> viewLevels = new ArrayList<>(tree.levels.size());

        for (Level level : tree.levels) {
            Item expandedItem = null;
            Item selectedItem = null;
            boolean isAllItemsAreSelectedChildes = true;
            for (Item item : level.items) {
                if (item.isExpanded) {
                    expandedItem = item;
                }
                if (item.isSelected) {
                    selectedItem = item;
                }
                if (!(Objects.equals(item.parentId, tree.id))) {
                    isAllItemsAreSelectedChildes = false;
                }
            }

            if (selectedItem != null) {
                viewLevels.add(new DetailedTreeViewLevel(level, selectedItem));
            } else if (expandedItem != null) {
                viewLevels.add(new ShortenedTreeViewLevel(level, expandedItem));
            } else if (isAllItemsAreSelectedChildes) {
                viewLevels.add(new ListItemsTreeViewLevel(level));
            } // else skip current level
        }

        return viewLevels;
    }
}
