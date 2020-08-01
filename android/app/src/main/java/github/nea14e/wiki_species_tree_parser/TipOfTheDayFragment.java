package github.nea14e.wiki_species_tree_parser;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import github.nea14e.wiki_species_tree_parser.models.TipOfTheDay;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class TipOfTheDayFragment extends BaseFragment {

    private TextView tipMessageTxt;
    private Button nextTipButton;
    private Button okButton;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        return inflater.inflate(R.layout.tip_of_the_day, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);
        tipMessageTxt = getView().findViewById(R.id.tip_message_txt);
        nextTipButton = getView().findViewById(R.id.next_tip_btn);
        nextTipButton.setOnClickListener(view1 -> this.getTipOfTheDay());
        okButton = getView().findViewById(R.id.ok_btn);
        // TODO okButton.setOnClickListener();
        getTipOfTheDay();
    }

    private void getTipOfTheDay() {
        retrofitHelper.api.getTipOfTheDay().enqueue(new Callback<TipOfTheDay>() {
            @Override
            public void onResponse(@NonNull Call<TipOfTheDay> call, @NonNull Response<TipOfTheDay> response) {
                TipOfTheDay data = response.body();
                tipMessageTxt.setText(data.tipText);
            }

            @Override
            public void onFailure(Call<TipOfTheDay> call, Throwable t) {
                TipOfTheDay data = new TipOfTheDay();
                data.tipText = t.getLocalizedMessage();
                tipMessageTxt.setText(data.tipText);
            }
        });
    }
}
