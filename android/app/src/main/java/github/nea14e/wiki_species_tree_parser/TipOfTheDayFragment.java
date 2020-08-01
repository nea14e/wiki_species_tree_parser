package github.nea14e.wiki_species_tree_parser;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import org.greenrobot.eventbus.EventBus;

import butterknife.BindView;
import butterknife.ButterKnife;
import butterknife.OnClick;
import butterknife.Unbinder;
import github.nea14e.wiki_species_tree_parser.models.TipOfTheDay;
import github.nea14e.wiki_species_tree_parser.network.SmartCallback;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class TipOfTheDayFragment extends BaseFragment {

    @BindView(R.id.tip_message_txt)
    TextView tipMessageTxt;
    @BindView(R.id.next_tip_btn)
    Button nextTipButton;
    @BindView(R.id.ok_btn)
    Button okButton;

    private Unbinder unbinder;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.tip_of_the_day, container, false);
        unbinder = ButterKnife.bind(this, view);
        getTipOfTheDay();
        return view;
    }

    @OnClick(R.id.next_tip_btn)
    public void getTipOfTheDay() {
        retrofitHelper.api.getTipOfTheDay().enqueue(new SmartCallback<TipOfTheDay>(true) {
            @Override
            protected void onData(TipOfTheDay data) {
                tipMessageTxt.setText(data.tipText);
            }
        });
    }

    @OnClick(R.id.ok_btn)
    public void onOnClick() {
        // TODO okButton.setOnClickListener();
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        unbinder.unbind();
    }
}
