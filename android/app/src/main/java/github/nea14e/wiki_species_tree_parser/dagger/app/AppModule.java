package github.nea14e.wiki_species_tree_parser.dagger.app;

import dagger.Binds;
import dagger.Module;
import github.nea14e.wiki_species_tree_parser.libs.image_loading.ImageLoaderHelper;
import github.nea14e.wiki_species_tree_parser.libs.image_loading.impl.GlideImageLoaderHelper;
import github.nea14e.wiki_species_tree_parser.libs.network.NetworkHelper;
import github.nea14e.wiki_species_tree_parser.libs.network.impl.RetrofitNetworkHelper;

@Module
public abstract class AppModule {
    @AppScope
    @Binds
    public abstract ImageLoaderHelper getImageLoaderHelper(GlideImageLoaderHelper helper);

    @AppScope
    @Binds
    public abstract NetworkHelper getNetworkHelper(RetrofitNetworkHelper helper);
}
