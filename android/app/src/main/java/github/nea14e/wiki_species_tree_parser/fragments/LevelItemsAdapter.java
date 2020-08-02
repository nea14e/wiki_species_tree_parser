package github.nea14e.wiki_species_tree_parser.fragments;

import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.bumptech.glide.Glide;

import butterknife.BindView;
import butterknife.ButterKnife;
import butterknife.OnClick;
import github.nea14e.wiki_species_tree_parser.R;
import github.nea14e.wiki_species_tree_parser.models.Item;
import github.nea14e.wiki_species_tree_parser.models.Level;

public class LevelItemsAdapter extends RecyclerView.Adapter<LevelItemsAdapter.ListItemViewHolder> {

    private Level level;

    public void setData(Level level) {
        this.level = level;
    }

    @NonNull
    @Override
    public ListItemViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        return null;  // TODO
    }

    @Override
    public void onBindViewHolder(@NonNull ListItemViewHolder holder, int position) {
        // TODO
    }

    @Override
    public void onViewRecycled(@NonNull ListItemViewHolder holder) {
        super.onViewRecycled(holder);
        holder.recycleMe();
    }

    @Override
    public int getItemCount() {
        return level.items.size();
    }

    public static class ListItemViewHolder extends RecyclerView.ViewHolder {

        @BindView(R.id.image_view)
        ImageView imageView;
        @BindView(R.id.item_title)
        TextView itemTitle;
        @BindView(R.id.item_leaves_count)
        TextView itemLeavesCount;
        @BindView(R.id.item_expanded_img)
        ImageView itemExpandedImg;

        private boolean hasImage;

        public ListItemViewHolder(@NonNull View itemView) {
            super(itemView);
            ButterKnife.bind(this, itemView);
        }

        public void bindData(Item item) {
            imageView.setContentDescription(item.titleForLanguage);
            if (item.imageUrl != null) {
                Glide.with(imageView)
                        .load(item.imageUrl)
                        .centerCrop()
                        .placeholder(R.color.border)
                        .into(imageView);
                hasImage = true;
            } else {
                Glide.with(imageView)
                        .clear(imageView);
                hasImage = false;
            }
            itemTitle.setText(item.titleForLanguage);
            itemLeavesCount.setText(item.leavesCount.toString());
            if (item.leavesCount > 0) {
                itemExpandedImg.setVisibility(View.VISIBLE);
            } else {
                itemExpandedImg.setVisibility(View.INVISIBLE);
            }
        }

        public void recycleMe() {
            if (hasImage) {
                Glide.with(imageView)
                        .clear(imageView);
                hasImage = false;
            }
        }

        @OnClick(R.id.level_item_layout)
        public void onLayoutClick() {
            // TODO expand/collapse tree
        }

        @OnClick(R.id.wiki_btn)
        public void onWikiBtnClick() {
            // TODO show wiki on current language (links' mask are in Config.py)
        }

        @OnClick(R.id.show_fullscreen_image_btn)
        public void onShowFillSizedImageBtnClick() {
            // TODO show full-screen image
        }
    }
}
