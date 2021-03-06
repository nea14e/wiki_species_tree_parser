package github.nea14e.wiki_species_tree_parser.libs.network.retrofit;

import java.util.List;

import github.nea14e.wiki_species_tree_parser.entities.Check;
import github.nea14e.wiki_species_tree_parser.entities.Level;
import github.nea14e.wiki_species_tree_parser.entities.SearchItem;
import github.nea14e.wiki_species_tree_parser.entities.TipOfTheDay;
import github.nea14e.wiki_species_tree_parser.entities.Tree;
import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Path;

public interface RetrofitApi {
    @GET("api/get_childes_by_id/{id}")
    Call<List<Level>> getChildesById(@Path("id") Long id);

    @GET("api/get_tree_by_id/{id}")
    Call<Tree> getTreeById(@Path("id") Long id);

    @GET("api/get_tree_default")
    Call<Tree> getTreeDefault();

    @GET("api/search_by_words/{words}/{offset}")
    Call<List<SearchItem>> searchByWords(@Path("words") String words, @Path("offset") int offset);

    @GET("api/get_tip_of_the_day")
    Call<TipOfTheDay> getTipOfTheDay();

    @GET("check")
    Call<Check> check();
}
