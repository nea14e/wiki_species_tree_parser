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
import github.nea14e.wiki_species_tree_parser.presenters.tree.view_entities.DetailedTreeViewLevel;

class DetailedLevelViewHolder extends BaseLevelViewHolder<DetailedTreeViewLevel> {

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

    public DetailedLevelViewHolder(@NonNull View levelView) {
        super(levelView);
        ButterKnife.bind(this, levelView);
    }

    @SuppressLint("SetTextI18n")
    public void bindData(DetailedTreeViewLevel viewLevel) {
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
    void recycleMe() {
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

    @OnClick(R.id.wiki_btn)
    public void onWikiBtn() {
        // TODO show wiki article
    }

    @OnClick(R.id.google_it_btn)
    public void onGoogleItBtn() {
        // TODO open browser with search query
    }

    @OnClick(R.id.bookmark_btn)
    public void onBookmarkBtn() {
        // TODO toggle bookmark state
    }

    @OnClick(R.id.share_btn)
    public void onShareBtn() {
        // TODO send share intent
    }
}
