package github.nea14e.wiki_species_tree_parser.logic.tree;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import java.util.List;
import java.util.Objects;

import github.nea14e.wiki_species_tree_parser.entities.Item;
import github.nea14e.wiki_species_tree_parser.entities.Level;
import github.nea14e.wiki_species_tree_parser.entities.Tree;
import github.nea14e.wiki_species_tree_parser.libs.network.NetworkHelper;
import github.nea14e.wiki_species_tree_parser.libs.network.SmartCallback;
import github.nea14e.wiki_species_tree_parser.libs.network.impl.RetrofitNetworkHelper;

public class OneSelectionTreeLogic implements TreeLogic {

    private final TreeLogic.Callback callback;

    @Nullable
    private Tree defaultTree;
    @Nullable
    private Tree tree;
    @Nullable
    private Level selectedLevel = null;
    @Nullable
    private Item selectedItem = null;

    private NetworkHelper networkHelper = new RetrofitNetworkHelper();

    public OneSelectionTreeLogic(@Nullable Long initId, Callback callback) {
        this.callback = callback;
        if (initId == null) {
            this.networkHelper.getTreeDefault(new SmartCallback<Tree>(true) {
                @Override
                protected void onData(Tree data) {
                    defaultTree = data;
                    tree = data;
                    callback.onNewTree(data);
                }
            });
        } else {
            this.networkHelper.getTreeById(initId, new SmartCallback<Tree>(true) {
                @Override
                protected void onData(Tree data) {
                    tree = data;
                    callback.onNewTree(data);
                }
            });
        }
    }

    @Override
    public void expandOrCollapse(long itemId) {
        if (tree == null)
            return;
        Level curLevel = null;
        Item curItem = null;
        for (Level level : tree.levels) {
            for (Item item : level.items) {
                if (item.id == itemId) {
                    curLevel = level;
                    curItem = item;
                    break;
                }
            }
            if (curItem != null) {
                break;
            }
        }
        if (curItem == null) {
            // If requested itemId not found in tree which exists now, reload entire tree
            this.networkHelper.getTreeById(itemId, new SmartCallback<Tree>(true) {
                @Override
                protected void onData(Tree data) {
                    tree = data;
                    callback.onNewTree(data);
                }
            });
            return;
        }

        // If selected item clicked - clear selection:
        if (selectedLevel != null && selectedItem == curItem) {
            deselectSelectedItem(curLevel, curItem);
            return;
        }  // If selected item clicked - end

        // Update isExpanded flags through the tree (required when user clicked on plain (not expanded) tree)
        updateExpanding(curLevel, curItem);

        // Deselect old
        if (selectedLevel != null && selectedLevel != curLevel) {
            selectedLevel.isLevelHasSelectedItem = false;
        }
        if (selectedItem != null && selectedItem != curItem) {
            selectedItem.isSelected = false;
        }

        // Select
        tree.id = curItem.id;
        curLevel.isLevelHasSelectedItem = true;
        curItem.isExpanded = true;
        curItem.isSelected = true;
        selectedLevel = curLevel;
        selectedItem = curItem;

        final Level finalCurLevel = curLevel;
        final Item finalCurItem = curItem;
        networkHelper.getChildesById(curItem.id, new SmartCallback<List<Level>>(false) {
            @Override
            protected void onData(List<Level> data) {
                updateSubtree(finalCurLevel, finalCurItem, data);
            }
        });
    }

    private void deselectSelectedItem(@NonNull Level curLevel, @NonNull Item curItem) {
        if (tree == null || selectedLevel == null || selectedItem == null)
            return;

        // Clear selection
        selectedLevel.isLevelHasSelectedItem = false;
        selectedItem.isSelected = false;
        selectedItem.isExpanded = false;

        // Select item's parent
        if (curItem.parentId != null) {
            boolean isBreak = false;
            for (Level level : tree.levels) {
                for (Item item : level.items) {
                    if (item.id == curItem.parentId) {
                        tree.id = item.id;
                        level.isLevelHasSelectedItem = true;
                        item.isSelected = true;
                        item.isExpanded = true;
                        updateSubtree(level, item, null);
                        return;
                    }
                }
            }
        }

        // If curItem have no parents - clear the tree to default state
        if (defaultTree != null) {
            tree = defaultTree;
            callback.onNewTree(defaultTree);
        } else {
            this.networkHelper.getTreeDefault(new SmartCallback<Tree>(true) {
                @Override
                protected void onData(Tree data) {
                    defaultTree = tree;
                    tree = data;
                    callback.onNewTree(data);
                }
            });
        }
    }

    private void updateExpanding(@NonNull Level curLevel, @NonNull Item curItem) {
        if (tree == null)
            return;

        long curId = curItem.id;
        for (int i = tree.levels.size() - 1; i >= 0; --i) {
            Level level = tree.levels.get(i);
            for (Item item : level.items) {
                if (item.id == curId) {
                    item.isExpanded = true;
                    if (item.parentId != null) {
                        curId = item.parentId;
                    } else {
                        return;  // Top levels without parent reached
                    }
                } else {
                    item.isExpanded = false;
                }
            }
        }
        return;
    }

    private void updateSubtree(@NonNull Level curLevel, @NonNull Item curItem, @Nullable List<Level> newLevels) {
        if (tree == null)
            return;

        int curLevelInd = tree.levels.indexOf(curLevel);

        // Delete all levels from the end of the tree if they parent is distinct from curItem.parentId
        for (int i = tree.levels.size() - 1; i > curLevelInd; --i) {
            Level level = tree.levels.get(i);
            if (Objects.equals(level.levelParentId, curItem.parentId)) {
                break;  // stop deletion when reached levels with the same parent
            }
            tree.levels.remove(level);
        }

        // Insert new levels to the end of the tree
        if (newLevels != null) {
            tree.levels.addAll(newLevels);
        }

        // Callback
        callback.onNewTree(tree);  // TODO send per-element changes info
    }

}
