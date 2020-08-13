package github.nea14e.wiki_species_tree_parser.fragments.tree.levels;

import android.content.Context;
import android.view.View;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import butterknife.BindView;
import butterknife.ButterKnife;
import github.nea14e.wiki_species_tree_parser.R;
import github.nea14e.wiki_species_tree_parser.entities.Item;
import github.nea14e.wiki_species_tree_parser.fragments.tree.level_items.LevelItemsAdapter;
import github.nea14e.wiki_species_tree_parser.presenters.tree.view_entities.ListItemsTreeViewLevel;

class ListItemsLevelViewHolder extends BaseLevelViewHolder<ListItemsTreeViewLevel> implements LevelItemsAdapter.Callback {

    @BindView(R.id.level_type)
    TextView levelType;
    @BindView(R.id.level_items_recycler_view)
    RecyclerView recyclerView;

    private LevelItemsAdapter adapter;
    private final BaseLevelViewHolder.Callback callback;

    public ListItemsLevelViewHolder(@NonNull View levelView, BaseLevelViewHolder.Callback callback) {
        super(levelView);
        this.callback = callback;
        ButterKnife.bind(this, levelView);
        setupRecyclerView(levelView.getContext());
    }

    private void setupRecyclerView(Context context) {
        // use this setting to improve performance if you know that changes
        // in content do not change the layout size of the RecyclerView
        recyclerView.setHasFixedSize(true);

        // use a linear layout manager
        LinearLayoutManager layoutManager = new LinearLayoutManager(context, LinearLayoutManager.HORIZONTAL, false);
        recyclerView.setLayoutManager(layoutManager);

        // specify an adapter (see also next example)
        if (adapter == null) {
            adapter = new LevelItemsAdapter(this);
        }
        recyclerView.setAdapter(adapter);
    }

    public void bindData(ListItemsTreeViewLevel viewLevel) {
        levelType.setText(viewLevel.level.type);
        adapter.setData(viewLevel.level.items);
    }

    @Override
    void recycleMe() {
        // Do nothing
    }

    @Override
    public void onItemLayoutClick(Item item) {
        callback.onItemLayoutClick(item);
    }

    @Override
    public void onItemImageClick(Item item) {
        callback.onItemImageClick(item);
    }
}
