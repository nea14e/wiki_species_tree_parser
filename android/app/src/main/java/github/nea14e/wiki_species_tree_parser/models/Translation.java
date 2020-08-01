package github.nea14e.wiki_species_tree_parser.models;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class Translation {

    @SerializedName("comment")
    @Expose
    public String comment;
    @SerializedName("lang_key")
    @Expose
    public String langKey;
    @SerializedName("rank_word")
    @Expose
    public String rankWord;
    @SerializedName("site_title")
    @Expose
    public String siteTitle;
    @SerializedName("parent_word")
    @Expose
    public String parentWord;
    @SerializedName("search_word")
    @Expose
    public String searchWord;
    @SerializedName("authors_word")
    @Expose
    public String authorsWord;
    @SerializedName("authors_content")
    @Expose
    public String authorsContent;
    @SerializedName("site_description")
    @Expose
    public String siteDescription;
    @SerializedName("tip_of_the_day_word")
    @Expose
    public String tipOfTheDayWord;

    @Override
    public String toString() {
        return "Translation{" +
                "comment='" + comment + '\'' +
                ", langKey='" + langKey + '\'' +
                '}';
    }
}