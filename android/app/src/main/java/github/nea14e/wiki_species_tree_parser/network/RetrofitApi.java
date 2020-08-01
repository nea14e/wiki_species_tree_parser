package github.nea14e.wiki_species_tree_parser.network;

import java.util.List;

import github.nea14e.wiki_species_tree_parser.models.Check;
import github.nea14e.wiki_species_tree_parser.models.Level;
import github.nea14e.wiki_species_tree_parser.models.SearchItem;
import github.nea14e.wiki_species_tree_parser.models.Tree;
import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Path;

public interface RetrofitApi {
    @GET("api/get_childes_by_id/{id}")
    Call<List<Level>> get_childes_by_id(@Path("id") Long id);

    @GET("api/get_tree_by_id/{id}")
    Call<Tree> get_tree_by_id(@Path("id") Long id);

    @GET("api/get_tree_default")
    Call<Tree> get_tree_default();

    @GET("api/search_by_words/{words}/{offset}")
    Call<List<SearchItem>> searchByWords(@Path("words") String words, @Path("offset") int offset);

    @GET("api/get_tip_of_the_day")
    Call<Check> get_tip_of_the_day();

    @GET("check")
    Call<Check> check();
}
