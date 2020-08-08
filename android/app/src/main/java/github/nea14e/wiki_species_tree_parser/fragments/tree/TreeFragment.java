package github.nea14e.wiki_species_tree_parser.fragments.tree;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import butterknife.BindView;
import butterknife.ButterKnife;
import butterknife.Unbinder;
import github.nea14e.wiki_species_tree_parser.R;
import github.nea14e.wiki_species_tree_parser.fragments.BaseFragment;
import github.nea14e.wiki_species_tree_parser.libs.network.SmartCallback;
import github.nea14e.wiki_species_tree_parser.models.Tree;

public class TreeFragment extends BaseFragment {

    @BindView(R.id.levels_recycler_view)
    RecyclerView recyclerView;
    private LevelsAdapter adapter;

    private Unbinder unbinder;

    private Tree tree;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.tree, container, false);
        unbinder = ButterKnife.bind(this, view);
        setupRecyclerView();
        if (tree != null) {
            adapter.setData(tree);
        } else {
            loadTreeDefault();
        }
        return view;
    }

    private void setupRecyclerView() {
        // use this setting to improve performance if you know that changes
        // in content do not change the layout size of the RecyclerView
        recyclerView.setHasFixedSize(true);

        // use a linear layout manager
        LinearLayoutManager layoutManager = new LinearLayoutManager(getContext());
        recyclerView.setLayoutManager(layoutManager);

        // specify an adapter (see also next example)
        adapter = new LevelsAdapter();
        recyclerView.setAdapter(adapter);
    }

    private void loadTreeDefault() {
        this.networkHelper.getTreeDefault(new SmartCallback<Tree>(true) {
            @Override
            protected void onData(Tree data) {
                tree = data;
                adapter.setData(tree);
            }
        });
    }

    // TODO private Tree parseTree(Tree tree) - get selected item on each level to the level.selectedItem

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        unbinder.unbind();
    }

    public static class ShowTreeEvent {
        @Nullable
        public final Long id;

        public ShowTreeEvent(@Nullable Long id) {
            this.id = id;
        }
    }
}
