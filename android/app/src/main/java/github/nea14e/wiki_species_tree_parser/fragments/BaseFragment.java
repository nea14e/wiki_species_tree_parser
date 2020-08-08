package github.nea14e.wiki_species_tree_parser.fragments;

import android.os.Bundle;

import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

import github.nea14e.wiki_species_tree_parser.libs.network.NetworkHelper;
import github.nea14e.wiki_species_tree_parser.libs.network.impl.RetrofitNetworkHelper;

public class BaseFragment extends Fragment {

    protected NetworkHelper networkHelper;

    @Override
    public void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setRetainInstance(true);
        networkHelper = new RetrofitNetworkHelper();
    }
}
