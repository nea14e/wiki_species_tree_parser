package github.nea14e.wiki_species_tree_parser.fragments;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import com.bumptech.glide.Glide;

import butterknife.BindView;
import butterknife.ButterKnife;
import butterknife.OnClick;
import butterknife.Unbinder;
import github.nea14e.wiki_species_tree_parser.R;
import github.nea14e.wiki_species_tree_parser.models.TipOfTheDay;
import github.nea14e.wiki_species_tree_parser.network.SmartCallback;

public class TipOfTheDayFragment extends BaseFragment {

    @BindView(R.id.image_view)
    ImageView imageView;
    @BindView(R.id.read_more)
    Button readMoreBtn;
    @BindView(R.id.tip_message_txt)
    TextView tipMessageTxt;
    @BindView(R.id.next_tip_btn)
    Button nextTipButton;
    @BindView(R.id.ok_btn)
    Button okButton;

    private Unbinder unbinder;

    private TipOfTheDay tipOfTheDay;
    private static final String BUNDLE_TIP_OF_THE_DAY = "BUNDLE_TIP_OF_THE_DAY";

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.tip_of_the_day, container, false);
        unbinder = ButterKnife.bind(this, view);

        if (savedInstanceState != null) {
            tipOfTheDay = (TipOfTheDay) savedInstanceState.getSerializable(BUNDLE_TIP_OF_THE_DAY);
            updateView();
        } else {
            getNextTip();
        }

        return view;
    }

    @OnClick(R.id.next_tip_btn)
    public void getNextTip() {
        retrofitHelper.api.getTipOfTheDay().enqueue(new SmartCallback<TipOfTheDay>(true) {
            @Override
            protected void onData(TipOfTheDay data) {
                tipOfTheDay = data;
                updateView();
            }
        });
    }

    private void updateView() {
        tipMessageTxt.setText(tipOfTheDay.tipText);
        if (tipOfTheDay.imageUrl != null) {
            Glide.with(this)
                    .load(tipOfTheDay.imageUrl)
                    .centerCrop()
                    .placeholder(R.color.border)
                    .into(imageView);
            readMoreBtn.setEnabled(true);
        } else {
            Glide.with(this)
                    .clear(imageView);
            readMoreBtn.setEnabled(false);
        }
    }

    @OnClick(R.id.ok_btn)
    public void onOnClick() {
        // TODO okButton.setOnClickListener();
    }

    @Override
    public void onSaveInstanceState(@NonNull Bundle outState) {
        outState.putSerializable(BUNDLE_TIP_OF_THE_DAY, tipOfTheDay);
        super.onSaveInstanceState(outState);
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        unbinder.unbind();
    }
}
