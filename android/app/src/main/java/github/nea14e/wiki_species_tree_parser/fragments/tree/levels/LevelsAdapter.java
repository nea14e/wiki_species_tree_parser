package github.nea14e.wiki_species_tree_parser.fragments.tree.levels;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import java.util.List;

import github.nea14e.wiki_species_tree_parser.R;
import github.nea14e.wiki_species_tree_parser.entities.Item;
import github.nea14e.wiki_species_tree_parser.presenters.tree.view_entities.BaseTreeViewLevel;
import github.nea14e.wiki_species_tree_parser.presenters.tree.view_entities.DetailedTreeViewLevel;
import github.nea14e.wiki_species_tree_parser.presenters.tree.view_entities.ShortenedTreeViewLevel;
import github.nea14e.wiki_species_tree_parser.presenters.tree.view_entities.ListItemsTreeViewLevel;

public class LevelsAdapter extends RecyclerView.Adapter<BaseLevelViewHolder<?>> implements BaseLevelViewHolder.Callback {

    private final LevelsAdapter.Callback callback;
    private List<BaseTreeViewLevel> levels;

    public LevelsAdapter(LevelsAdapter.Callback callback) {
        this.callback = callback;
    }

    public void setData(List<BaseTreeViewLevel> levels) {
        this.levels = levels;
        notifyDataSetChanged();
    }

    @NonNull
    @Override
    public BaseLevelViewHolder<?> onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {// create a new view
        View v;
        switch (ViewTypes.values()[viewType]) {
            case Shortened:
                v = LayoutInflater.from(parent.getContext())
                        .inflate(R.layout.level_shortened, parent, false);
                return new ShortenedLevelViewHolder(v, this);
            case Detailed:
                v = LayoutInflater.from(parent.getContext())
                        .inflate(R.layout.level_detailed, parent, false);
                return new DetailedLevelViewHolder(v, this);
            case ListItems:
                v = LayoutInflater.from(parent.getContext())
                        .inflate(R.layout.level_list_items, parent, false);
                return new ListItemsLevelViewHolder(v, this);
            default:
                throw new IllegalStateException("LevelsAdapter: onCreateViewHolder() was called with invalid viewType.");
        }
    }

    @Override
    public void onBindViewHolder(@NonNull BaseLevelViewHolder holder, int position) {
        // - get element from your dataset at this position
        // - replace the contents of the view with that element
        BaseTreeViewLevel viewLevel = levels.get(position);
        if (holder instanceof ShortenedLevelViewHolder) {
            ((ShortenedLevelViewHolder) holder).bindData((ShortenedTreeViewLevel) viewLevel);
        } else if (holder instanceof DetailedLevelViewHolder) {
            ((DetailedLevelViewHolder) holder).bindData((DetailedTreeViewLevel) viewLevel);
        } else if (holder instanceof ListItemsLevelViewHolder) {
            ((ListItemsLevelViewHolder) holder).bindData((ListItemsTreeViewLevel) viewLevel);
        }
    }

    @Override
    public int getItemViewType(int position) {
        BaseTreeViewLevel viewLevel = levels.get(position);
        if (viewLevel instanceof ShortenedTreeViewLevel) {
            return ViewTypes.Shortened.ordinal();
        } else if (viewLevel instanceof DetailedTreeViewLevel) {
            return ViewTypes.Detailed.ordinal();
        } else if (viewLevel instanceof ListItemsTreeViewLevel) {
            return ViewTypes.ListItems.ordinal();
        }
        return super.getItemViewType(position);
    }

    @Override
    public int getItemCount() {
        if (levels == null)
            return 0;
        return levels.size();
    }

    @Override
    public void onItemLayoutClick(Item item) {
        callback.onItemLayoutClick(item);
    }

    @Override
    public void onItemImageClick(Item item) {
        callback.onItemImageClick(item);
    }

    private enum ViewTypes {
        Shortened, Detailed, ListItems
    }

    public interface Callback {
        void onItemLayoutClick(Item item);
        void onItemImageClick(Item item);
    }

}
