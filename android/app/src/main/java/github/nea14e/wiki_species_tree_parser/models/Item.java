package github.nea14e.wiki_species_tree_parser.models;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class Item {

    @SerializedName("id")
    @Expose
    public Long id;
    @SerializedName("page_url")
    @Expose
    public String pageUrl;
    @SerializedName("image_url")
    @Expose
    public String imageUrl;
    @SerializedName("parent_id")
    @Expose
    public Long parentId;
    @SerializedName("is_expanded")
    @Expose
    public Boolean isExpanded;
    @SerializedName("is_selected")
    @Expose
    public Boolean isSelected;
    @SerializedName("leaves_count")
    @Expose
    public Long leavesCount;
    @SerializedName("title_for_language")
    @Expose
    public String titleForLanguage;
    @SerializedName("wiki_url_for_language")
    @Expose
    public String wikiUrlForLanguage;

}
