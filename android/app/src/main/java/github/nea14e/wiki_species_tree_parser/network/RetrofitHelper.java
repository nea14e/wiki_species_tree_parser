package github.nea14e.wiki_species_tree_parser.network;

import okhttp3.OkHttpClient;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class RetrofitHelper {
    public final RetrofitApi api;

    public RetrofitHelper() {
        Retrofit retrofit = new Retrofit.Builder()
                .client(new OkHttpClient.Builder()
                        .addNetworkInterceptor(new RetrofitLanguageInterceptor())
                        .build()
                )
                .baseUrl("http://10.0.2.2:8000/")
                .addConverterFactory(GsonConverterFactory.create())
                .build();

        api = retrofit.create(RetrofitApi.class);
    }
}
