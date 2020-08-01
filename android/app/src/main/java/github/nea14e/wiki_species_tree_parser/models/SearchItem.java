package github.nea14e.wiki_species_tree_parser.models;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class SearchItem {

    @SerializedName("id")
    @Expose
    public Long id;
    @SerializedName("rank_for_language")
    @Expose
    public String rankForLanguage;
    @SerializedName("title_for_language")
    @Expose
    public String titleForLanguage;
    @SerializedName("image_url")
    @Expose
    public String imageUrl;
    @SerializedName("rank_order")
    @Expose
    public Long rankOrder;
    @SerializedName("leaves_count")
    @Expose
    public Long leavesCount;

}