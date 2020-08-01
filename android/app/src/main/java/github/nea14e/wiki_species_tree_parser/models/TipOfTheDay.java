package github.nea14e.wiki_species_tree_parser.models;

import java.io.Serializable;
import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class TipOfTheDay implements Serializable
{

    @SerializedName("id")
    @Expose
    public Long id;
    @SerializedName("tip_text")
    @Expose
    public String tipText;
    @SerializedName("species_id")
    @Expose
    public Long speciesId;
    @SerializedName("image_url")
    @Expose
    public String imageUrl;
    private final static long serialVersionUID = 172515541519708910L;

}
