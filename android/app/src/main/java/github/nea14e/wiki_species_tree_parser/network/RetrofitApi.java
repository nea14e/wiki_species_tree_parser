package github.nea14e.wiki_species_tree_parser.network;

import github.nea14e.wiki_species_tree_parser.models.Check;
import retrofit2.Call;
import retrofit2.http.GET;

public interface RetrofitApi {
    @GET("check")
    Call<Check> check();
}
