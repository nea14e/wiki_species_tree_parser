package github.nea14e.wiki_species_tree_parser.models;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class TipOfTheDay {

    @SerializedName("id")
    @Expose
    public Long id;
    @SerializedName("tip_text")
    @Expose
    public String tipText;
    @SerializedName("species_id")
    @Expose
    public String speciesId;
    @SerializedName("image_url")
    @Expose
    public String imageUrl;

}
