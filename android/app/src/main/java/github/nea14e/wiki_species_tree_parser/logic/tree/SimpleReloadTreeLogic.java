package github.nea14e.wiki_species_tree_parser.logic.tree;

import androidx.annotation.Nullable;

import github.nea14e.wiki_species_tree_parser.entities.Tree;
import github.nea14e.wiki_species_tree_parser.libs.network.NetworkHelper;
import github.nea14e.wiki_species_tree_parser.libs.network.SmartCallback;
import github.nea14e.wiki_species_tree_parser.libs.network.impl.RetrofitNetworkHelper;

public class SimpleReloadTreeLogic implements TreeLogic {

    private final Callback callback;

    @Nullable
    private Tree tree;

    private NetworkHelper networkHelper = new RetrofitNetworkHelper();

    public SimpleReloadTreeLogic(@Nullable Long initId, Callback callback) {
        this.callback = callback;
        if (initId == null) {
            this.networkHelper.getTreeDefault(new SmartCallback<Tree>(true) {
                @Override
                protected void onData(Tree data) {
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

        this.networkHelper.getTreeById(itemId, new SmartCallback<Tree>(true) {
            @Override
            protected void onData(Tree data) {
                tree = data;
                callback.onNewTree(data);
            }
        });
    }

}
