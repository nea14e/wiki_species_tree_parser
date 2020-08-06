package github.nea14e.wiki_species_tree_parser.libs.image_loading;

import android.widget.ImageView;

public interface ImageLoaderHelper {
    void loadImage(String url, boolean isCenterCrop, ImageView imageView);
    void clearImage(ImageView imageView);
}
