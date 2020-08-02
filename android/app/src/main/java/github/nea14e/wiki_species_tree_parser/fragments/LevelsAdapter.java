package github.nea14e.wiki_species_tree_parser.fragments;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import butterknife.BindView;
import butterknife.ButterKnife;
import github.nea14e.wiki_species_tree_parser.R;
import github.nea14e.wiki_species_tree_parser.models.Level;
import github.nea14e.wiki_species_tree_parser.models.Tree;

public class LevelsAdapter extends RecyclerView.Adapter<LevelsAdapter.ExpandedLevelViewHolder> {

    private Tree tree;

    public void setData(Tree data) {
        this.tree = data;
    }

    @NonNull
    @Override
    public ExpandedLevelViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {// create a new view
        View v = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.level_expanded, parent, false);
        return new ExpandedLevelViewHolder(v);
    }

    @Override
    public void onBindViewHolder(@NonNull ExpandedLevelViewHolder holder, int position) {
        // - get element from your dataset at this position
        // - replace the contents of the view with that element
        holder.bindData(this.tree.levels.get(position));
    }

    @Override
    public int getItemCount() {
        return tree.levels.size();
    }

    public static class ExpandedLevelViewHolder extends RecyclerView.ViewHolder {

        @BindView(R.id.level_type)
        TextView levelType;
        @BindView(R.id.level_items_recycler_view)
        RecyclerView recyclerView;

        private LevelItemsAdapter adapter;

        public ExpandedLevelViewHolder(@NonNull View levelView) {
            super(levelView);
            ButterKnife.bind(this, levelView);
            setupRecyclerView(levelView.getContext());
        }

        private void setupRecyclerView(Context context) {
            // use this setting to improve performance if you know that changes
            // in content do not change the layout size of the RecyclerView
            recyclerView.setHasFixedSize(true);

            // use a linear layout manager
            LinearLayoutManager layoutManager = new LinearLayoutManager(context);
            recyclerView.setLayoutManager(layoutManager);

            // specify an adapter (see also next example)
            if (adapter == null) {
                adapter = new LevelItemsAdapter();
            }
            recyclerView.setAdapter(adapter);
        }

        public void bindData(Level level) {
            levelType.setText(level.titleOnLanguage);
            adapter.setData(level);
            recyclerView.invalidate();
        }
    }
}
