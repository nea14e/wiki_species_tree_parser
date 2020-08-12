package github.nea14e.wiki_species_tree_parser.fragments.tree.levels;

import android.view.View;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import github.nea14e.wiki_species_tree_parser.presenters.tree.view_entities.BaseTreeViewLevel;

abstract class BaseLevelViewHolder<T extends BaseTreeViewLevel> extends RecyclerView.ViewHolder {
    public BaseLevelViewHolder(@NonNull View itemView) {
        super(itemView);
    }

    abstract void bindData(T viewLevel);

    abstract void recycleMe();
}
