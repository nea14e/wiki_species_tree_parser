package github.nea14e.wiki_species_tree_parser.models;

import java.util.List;
import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class Level {

    @SerializedName("type")
    @Expose
    public String type;
    @SerializedName("items")
    @Expose
    public List<Item> items = null;
    @SerializedName("title_on_language")
    @Expose
    public String titleOnLanguage;
    @SerializedName("level_parent_title")
    @Expose
    public Object levelParentTitle;
    @SerializedName("is_level_has_selected_item")
    @Expose
    public Boolean isLevelHasSelectedItem;

}
