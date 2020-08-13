package github.nea14e.wiki_species_tree_parser.fragments.tree.level_items;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import java.util.List;

import github.nea14e.wiki_species_tree_parser.R;
import github.nea14e.wiki_species_tree_parser.entities.Item;

public class LevelItemsAdapter extends RecyclerView.Adapter<ListItemViewHolder> implements ListItemViewHolder.Callback {

    private List<Item> items;
    private final LevelItemsAdapter.Callback callback;

    public LevelItemsAdapter(LevelItemsAdapter.Callback callback) {
        this.callback = callback;
    }

    public void setData(List<Item> items) {
        this.items = items;
        notifyDataSetChanged();
    }

    @NonNull
    @Override
    public ListItemViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View v = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.level_item, parent, false);
        return new ListItemViewHolder(v, this);
    }

    @Override
    public void onBindViewHolder(@NonNull ListItemViewHolder holder, int position) {
        holder.bindData(items.get(position));
    }

    @Override
    public void onViewRecycled(@NonNull ListItemViewHolder holder) {
        super.onViewRecycled(holder);
        holder.recycleMe();
    }

    @Override
    public int getItemCount() {
        if (items == null)
            return 0;
        return items.size();
    }

    @Override
    public void onItemLayoutClick(Item item) {
        callback.onItemLayoutClick(item);
    }

    @Override
    public void onItemImageClick(Item item) {
        callback.onItemImageClick(item);
    }

    public interface Callback {
        void onItemLayoutClick(Item item);
        void onItemImageClick(Item item);
    }
}
