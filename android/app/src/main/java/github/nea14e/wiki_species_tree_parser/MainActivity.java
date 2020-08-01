package github.nea14e.wiki_species_tree_parser;

import android.os.Bundle;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ProgressBar;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentManager;
import androidx.fragment.app.FragmentTransaction;

import org.greenrobot.eventbus.EventBus;
import org.greenrobot.eventbus.Subscribe;
import org.greenrobot.eventbus.ThreadMode;

import butterknife.BindView;
import butterknife.ButterKnife;
import github.nea14e.wiki_species_tree_parser.network.SmartCallback;

public class MainActivity extends AppCompatActivity {

    private enum States {
        TipOfTheDay, Tree, Search, Info
    }
    private States state;
    private Fragment fragment;

    @BindView(R.id.fragment_container)
    ViewGroup fragmentContainer;
    @BindView(R.id.wait_progress_bar)
    ProgressBar progressBar;

    private static final String BUNDLE_STATE = "state";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        ButterKnife.bind(this);

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
        new AlertDialog.Builder(this)
                .setMessage(event.message)
                .setPositiveButton(R.string.ok_btn, (dialogInterface, i) -> dialogInterface.dismiss())
                .create()
                .show();
    }

    @Override
    protected void onStop() {
        super.onStop();
        EventBus.getDefault().unregister(this);
    }

    public static class StartLongOperationEvent {
    }

    public static class StopLongOperationEvent {
    }
}