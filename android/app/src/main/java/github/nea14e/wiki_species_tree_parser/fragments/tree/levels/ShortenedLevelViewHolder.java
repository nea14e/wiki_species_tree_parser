package github.nea14e.wiki_species_tree_parser.fragments.tree.levels;

import android.annotation.SuppressLint;
import android.view.View;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.annotation.NonNull;

import butterknife.BindView;
import butterknife.ButterKnife;
import butterknife.OnClick;
import github.nea14e.wiki_species_tree_parser.R;
import github.nea14e.wiki_species_tree_parser.libs.image_loading.ImageLoaderHelper;
import github.nea14e.wiki_species_tree_parser.libs.image_loading.impl.GlideImageLoaderHelper;
import github.nea14e.wiki_species_tree_parser.presenters.tree.view_entities.ShortenedTreeViewLevel;

class ShortenedLevelViewHolder extends BaseLevelViewHolder<ShortenedTreeViewLevel> {

    @BindView(R.id.image_view)
    ImageView imageView;
    @BindView(R.id.level_type)
    TextView levelType;
    @BindView(R.id.level_item_title)
    TextView levelItemTitle;
    @BindView(R.id.level_item_leaves_count)
    TextView itemLeavesCount;

    private boolean hasImage = false;

    ImageLoaderHelper imageLoadHelper = new GlideImageLoaderHelper();

    public ShortenedLevelViewHolder(@NonNull View levelView) {
        super(levelView);
        ButterKnife.bind(this, levelView);
    }

    @SuppressLint("SetTextI18n")
    public void bindData(ShortenedTreeViewLevel viewLevel) {
        imageView.setContentDescription(viewLevel.item.titleForLanguage);
        if (viewLevel.item.imageUrl != null) {
            imageLoadHelper.loadImage(viewLevel.item.imageUrl, true, imageView);
            hasImage = true;
        } else {
            imageLoadHelper.clearImage(imageView);
            hasImage = false;
        }
        levelType.setText(viewLevel.level.titleOnLanguage);
        levelItemTitle.setText(viewLevel.item.titleForLanguage);
        if (viewLevel.item.leavesCount != null && viewLevel.item.leavesCount > 0) {
            itemLeavesCount.setText(viewLevel.item.leavesCount.toString());
        } else {
            itemLeavesCount.setText("?");
        }
    }

    @Override
    public void recycleMe() {
        if (hasImage) {
            imageLoadHelper.clearImage(imageView);
            hasImage = false;
        }
    }

    @OnClick(R.id.level_item_layout)
    public void onLayoutClick() {
        // TODO expand/collapse tree
    }

    @OnClick(R.id.image_view)
    public void onImageClick() {
        // TODO show full-screen image
    }
}
