package github.nea14e.wiki_species_tree_parser.libs.network.impl;

import java.util.List;

import javax.inject.Inject;

import github.nea14e.wiki_species_tree_parser.libs.network.retrofit.RetrofitApi;
import github.nea14e.wiki_species_tree_parser.libs.network.retrofit.RetrofitLanguageInterceptor;
import github.nea14e.wiki_species_tree_parser.libs.network.SmartCallback;
import github.nea14e.wiki_species_tree_parser.entities.Check;
import github.nea14e.wiki_species_tree_parser.entities.Level;
import github.nea14e.wiki_species_tree_parser.entities.SearchItem;
import github.nea14e.wiki_species_tree_parser.entities.TipOfTheDay;
import github.nea14e.wiki_species_tree_parser.entities.Tree;
import okhttp3.OkHttpClient;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class RetrofitNetworkHelper extends BaseNetworkHelper {
    private final RetrofitApi api;

    @Inject
    public RetrofitNetworkHelper() {
        Retrofit retrofit = new Retrofit.Builder()
                .client(new OkHttpClient.Builder()
                        .addNetworkInterceptor(new RetrofitLanguageInterceptor())
                        .build()
                )
                .baseUrl(super.BASE_URL)
                .addConverterFactory(GsonConverterFactory.create())
                .build();

        api = retrofit.create(RetrofitApi.class);
    }

    public void getChildesById(Long id, SmartCallback<List<Level>> callback) {
        api.getChildesById(id)
                .enqueue(callback);
    }

    public void getTreeById(Long id, SmartCallback<Tree> callback) {
        api.getTreeById(id)
                .enqueue(callback);
    }

    public void getTreeDefault(SmartCallback<Tree> callback) {
        api.getTreeDefault()
                .enqueue(callback);
    }

    public void searchByWords(String words, int offset, SmartCallback<List<SearchItem>> callback) {
        api.searchByWords(words, offset)
                .enqueue(callback);
    }

    public void getTipOfTheDay(SmartCallback<TipOfTheDay> callback) {
        api.getTipOfTheDay()
                .enqueue(callback);
    }

    public void check(SmartCallback<Check> callback) {
        api.check()
                .enqueue(callback);
    }
}
