package github.nea14e.wiki_species_tree_parser.fragments;

import android.os.Bundle;
import android.os.Handler;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import org.greenrobot.eventbus.EventBus;

import butterknife.ButterKnife;
import butterknife.OnClick;
import butterknife.Unbinder;
import github.nea14e.wiki_species_tree_parser.MainActivity;
import github.nea14e.wiki_species_tree_parser.R;
import github.nea14e.wiki_species_tree_parser.models.Check;
import github.nea14e.wiki_species_tree_parser.network.SmartCallback;

public class NoNetworkFragment extends BaseFragment {

    private Unbinder unbinder;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.no_network, container, false);
        unbinder = ButterKnife.bind(this, view);
        return view;
    }

    @OnClick(R.id.retry_btn)
    public void checkConnection() {
        EventBus.getDefault().post(new MainActivity.StartLongOperationEvent());
        Handler handler = new Handler();
        handler.postDelayed(new Runnable() {
            @Override
            public void run() {
                retrofitHelper.api.check().enqueue(new SmartCallback<Check>(true) {
                    @Override
                    protected void onData(Check data) {
                        if (data.allIsOk) {
                            EventBus.getDefault().post(new OnNetworkRestoredEvent());
                        }
                    }
                });
            }
        }, 1000);
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        unbinder.unbind();
    }

    public static class OnNetworkRestoredEvent {
    }
}
