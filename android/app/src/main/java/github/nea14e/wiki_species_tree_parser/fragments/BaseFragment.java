package github.nea14e.wiki_species_tree_parser.fragments;

import android.os.Bundle;

import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

import javax.inject.Inject;

import github.nea14e.wiki_species_tree_parser.App;
import github.nea14e.wiki_species_tree_parser.libs.network.NetworkHelper;

public class BaseFragment extends Fragment {

    @Inject
    protected NetworkHelper networkHelper;

    @Override
    public void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setRetainInstance(true);
        App.getAppComponent().inject(this);
    }
}
