package github.nea14e.wiki_species_tree_parser.network;

import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class RetrofitHelper {
    public final RetrofitApi api;

    public RetrofitHelper() {
        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl("http://10.0.2.2:8000/")
                .addConverterFactory(GsonConverterFactory.create())
                .build();

        api = retrofit.create(RetrofitApi.class);
    }
}
