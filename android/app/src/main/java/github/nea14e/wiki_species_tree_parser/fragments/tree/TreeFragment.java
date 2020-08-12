package github.nea14e.wiki_species_tree_parser.fragments.tree;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import java.util.List;

import butterknife.BindView;
import butterknife.ButterKnife;
import butterknife.Unbinder;
import github.nea14e.wiki_species_tree_parser.R;
import github.nea14e.wiki_species_tree_parser.fragments.BaseFragment;
import github.nea14e.wiki_species_tree_parser.fragments.tree.levels.LevelsAdapter;
import github.nea14e.wiki_species_tree_parser.presenters.tree.ThreeTypesTreePresenter;
import github.nea14e.wiki_species_tree_parser.presenters.tree.TreePresenter;
import github.nea14e.wiki_species_tree_parser.presenters.tree.view_entities.BaseTreeViewLevel;

public class TreeFragment extends BaseFragment implements TreePresenter.Callback {

    @BindView(R.id.levels_recycler_view)
    RecyclerView recyclerView;
    private LevelsAdapter adapter;

    private Unbinder unbinder;

    private TreePresenter presenter = new ThreeTypesTreePresenter(null, this);

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.tree, container, false);
        unbinder = ButterKnife.bind(this, view);
        setupRecyclerView();
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

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        unbinder.unbind();
    }

    @Override
    public void onNewTree(List<BaseTreeViewLevel> viewLevels) {
        adapter.setData(viewLevels);
    }

    public static class ShowTreeEvent {
        @Nullable
        public final Long id;

        public ShowTreeEvent(@Nullable Long id) {
            this.id = id;
        }
    }
}
