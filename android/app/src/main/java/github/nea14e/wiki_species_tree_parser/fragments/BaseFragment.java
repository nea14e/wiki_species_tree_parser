package github.nea14e.wiki_species_tree_parser.fragments;

import android.os.Bundle;

import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

import github.nea14e.wiki_species_tree_parser.network.RetrofitHelper;

public class BaseFragment extends Fragment {

    protected RetrofitHelper retrofitHelper;

    @Override
    public void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        retrofitHelper = new RetrofitHelper();
    }
}
