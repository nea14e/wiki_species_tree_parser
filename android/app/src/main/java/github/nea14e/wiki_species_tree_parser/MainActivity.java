package github.nea14e.wiki_species_tree_parser;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.content.ContextCompat;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentManager;
import androidx.fragment.app.FragmentTransaction;

import android.content.pm.PackageManager;
import android.os.Bundle;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ProgressBar;
import android.widget.TextView;

import github.nea14e.wiki_species_tree_parser.models.Check;
import github.nea14e.wiki_species_tree_parser.models.Tree;
import github.nea14e.wiki_species_tree_parser.network.RetrofitHelper;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class MainActivity extends AppCompatActivity {

    private enum States {
        TipOfTheDay, Tree, Search, Info
    }
    private States state;
    private Fragment fragment;

    private ViewGroup fragmentContainer;
    //private ProgressBar progressBar;

    private static final String BUNDLE_STATE = "state";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        fragmentContainer = findViewById(R.id.fragment_container);
        //progressBar = findViewById(R.id.wait_progress_bar);


        if (savedInstanceState != null) {
            state = States.valueOf(savedInstanceState.getString(BUNDLE_STATE));
        } else {
            state = States.TipOfTheDay;
        }

        switch (state) {
            case TipOfTheDay:
                fragment = new TipOfTheDayFragment();
                break;
            default:
                fragment = new Fragment();
                break;
        }

        FragmentManager fragmentManager = getSupportFragmentManager();
        FragmentTransaction fragmentTransaction = fragmentManager.beginTransaction();
        fragmentTransaction.add(R.id.fragment_container, fragment);
        fragmentTransaction.commit();
    }
}