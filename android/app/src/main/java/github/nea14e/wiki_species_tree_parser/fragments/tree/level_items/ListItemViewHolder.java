package github.nea14e.wiki_species_tree_parser.fragments.tree.level_items;

import android.annotation.SuppressLint;
import android.view.View;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import butterknife.BindView;
import butterknife.ButterKnife;
import butterknife.OnClick;
import github.nea14e.wiki_species_tree_parser.R;
import github.nea14e.wiki_species_tree_parser.entities.Item;
import github.nea14e.wiki_species_tree_parser.libs.image_loading.ImageLoaderHelper;
import github.nea14e.wiki_species_tree_parser.libs.image_loading.impl.GlideImageLoaderHelper;

class ListItemViewHolder extends RecyclerView.ViewHolder {

    @BindView(R.id.image_view)
    ImageView imageView;
    @BindView(R.id.item_title)
    TextView itemTitle;
    @BindView(R.id.item_leaves_count)
    TextView itemLeavesCount;

    private boolean hasImage = false;

    ImageLoaderHelper imageLoadHelper = new GlideImageLoaderHelper();

    private Item item;
    private final ListItemViewHolder.Callback callback;

    public ListItemViewHolder(@NonNull View itemView, ListItemViewHolder.Callback callback) {
        super(itemView);
        this.callback = callback;
        ButterKnife.bind(this, itemView);
    }

    @SuppressLint("SetTextI18n")
    public void bindData(Item item) {
        this.item = item;
        imageView.setContentDescription(item.titleForLanguage);
        if (item.imageUrl != null) {
            imageLoadHelper.loadImage(item.imageUrl, true, imageView);
            hasImage = true;
        } else {
            imageLoadHelper.clearImage(imageView);
            hasImage = false;
        }
        itemTitle.setText(item.titleForLanguage);
        if (item.leavesCount != null && item.leavesCount > 0) {
            itemLeavesCount.setText(item.leavesCount.toString());
        } else {
            itemLeavesCount.setText("?");
        }
    }

    public void recycleMe() {
        if (hasImage) {
            imageLoadHelper.clearImage(imageView);
            hasImage = false;
        }
        this.item = null;
    }

    @OnClick(R.id.level_item_layout)
    public void onLayoutClick() {
        callback.onItemLayoutClick(item);
    }

    @OnClick(R.id.image_view)
    public void onImageClick() {
        callback.onItemImageClick(item);
    }

    public interface Callback {
        void onItemLayoutClick(Item item);
        void onItemImageClick(Item item);
    }
}
