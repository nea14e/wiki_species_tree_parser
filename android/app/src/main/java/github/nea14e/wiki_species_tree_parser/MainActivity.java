package github.nea14e.wiki_species_tree_parser;

import android.os.Bundle;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ProgressBar;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentManager;
import androidx.fragment.app.FragmentTransaction;

import org.greenrobot.eventbus.EventBus;
import org.greenrobot.eventbus.Subscribe;
import org.greenrobot.eventbus.ThreadMode;

import butterknife.BindView;
import butterknife.ButterKnife;
import github.nea14e.wiki_species_tree_parser.fragments.NoNetworkFragment;
import github.nea14e.wiki_species_tree_parser.fragments.TipOfTheDayFragment;
import github.nea14e.wiki_species_tree_parser.network.SmartCallback;

public class MainActivity extends AppCompatActivity {

    private enum State {
        TipOfTheDay, Tree, Search, Authors, NoNetwork
    }
    private State state;
    private Fragment fragment;

    @BindView(R.id.fragment_container)
    ViewGroup fragmentContainer;
    @BindView(R.id.wait_progress_bar)
    ProgressBar progressBar;

    private static final String BUNDLE_STATE = "BUNDLE_STATE";
    private static final String MAIN_FRAGMENT_TAG = "MAIN_FRAGMENT_TAG";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        ButterKnife.bind(this);

        if (savedInstanceState != null) {
            this.state = State.valueOf(savedInstanceState.getString(BUNDLE_STATE));
            FragmentManager fragmentManager = getSupportFragmentManager();
            this.fragment = fragmentManager.findFragmentByTag(MAIN_FRAGMENT_TAG);
        } else {
            this.state = State.TipOfTheDay;
            switchFragment(this.state);
        }
    }

    private void switchFragment(State state) {
        this.state = state;

        FragmentManager fragmentManager = getSupportFragmentManager();
        FragmentTransaction fragmentTransaction = fragmentManager.beginTransaction();
        if (this.fragment != null) {
            fragmentTransaction.remove(this.fragment);
        }
        switch (state) {
            case TipOfTheDay:
                fragment = new TipOfTheDayFragment();
                break;
            case NoNetwork:
                fragment = new NoNetworkFragment();
                break;
            default:  // TODO
                fragment = new Fragment();
                break;
        }
        fragmentTransaction.add(R.id.fragment_container, fragment, MAIN_FRAGMENT_TAG);
        fragmentTransaction.commit();
    }

    @Override
    protected void onStart() {
        super.onStart();
        EventBus.getDefault().register(this);
    }

    @Subscribe(threadMode = ThreadMode.MAIN)
    public void onStartLongOperation(StartLongOperationEvent event) {
        progressBar.setVisibility(View.VISIBLE);
    }

    @Subscribe(threadMode = ThreadMode.MAIN)
    public void onStopLongOperation(StopLongOperationEvent event) {
        progressBar.setVisibility(View.GONE);
    }

    @Subscribe(threadMode = ThreadMode.MAIN)
    public void onNetworkErrorEvent(SmartCallback.OnNetworkErrorEvent event) {
        progressBar.setVisibility(View.GONE);
        switchFragment(State.NoNetwork);
    }

    @Subscribe(threadMode = ThreadMode.MAIN)
    public void onNetworkRestoredEvent(NoNetworkFragment.OnNetworkRestoredEvent event) {
        switchFragment(State.TipOfTheDay);  // TODO switch to State.Tree
    }

    @Override
    protected void onStop() {
        super.onStop();
        EventBus.getDefault().unregister(this);
    }

    @Override
    protected void onSaveInstanceState(@NonNull Bundle outState) {
        outState.putString(BUNDLE_STATE, state.name());
        super.onSaveInstanceState(outState);
    }

    public static class StartLongOperationEvent {
    }

    public static class StopLongOperationEvent {
    }
}