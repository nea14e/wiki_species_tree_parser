package github.nea14e.wiki_species_tree_parser;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import androidx.annotation.NonNull;
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
