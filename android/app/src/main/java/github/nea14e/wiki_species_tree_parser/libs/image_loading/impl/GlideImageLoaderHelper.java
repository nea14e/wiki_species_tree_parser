package github.nea14e.wiki_species_tree_parser.libs.image_loading.impl;

import android.graphics.drawable.Drawable;
import android.widget.ImageView;

import com.bumptech.glide.Glide;
import com.bumptech.glide.RequestBuilder;

import github.nea14e.wiki_species_tree_parser.R;

public class GlideImageLoaderHelper extends BaseImageLoaderHelper {
    public void loadImage(String url, boolean isCenterCrop, ImageView imageView) {

        // TODO troubles with Wikimedia URL's
        String[] urls = new String[] {
                "https://hsto.org/webt/e3/xm/af/e3xmafztka0bp04mxq5ucubnrse.jpeg",
                "https://hsto.org/webt/h_/7i/1q/h_7i1qdi64b2yvnmovms07o6etg.png",
                "https://hsto.org/webt/pb/fs/qi/pbfsqi8eth0t8sgl31y0uwng-1o.jpeg",
                "https://hsto.org/getpro/habr/post_images/7e6/e9e/2d7/7e6e9e2d7c5d37c4359e510430c2cdc9.jpg",
                "https://hsto.org/webt/oq/49/dv/oq49dvodxnylv1tpofzo6jtjnqk.jpeg"
        };
        url = urls[Math.abs(url.hashCode()) % urls.length];  // one input url always will result the same output url

        RequestBuilder<Drawable> load = Glide.with(imageView.getContext())
                .load(url);
        if (isCenterCrop) {
            load = load.centerCrop();
        }

        load.placeholder(R.color.border)
                .error(android.R.color.holo_red_dark)
                .into(imageView);
    }

    public void clearImage(ImageView imageView) {
        Glide.with(imageView.getContext())
                .clear(imageView);
    }
}
