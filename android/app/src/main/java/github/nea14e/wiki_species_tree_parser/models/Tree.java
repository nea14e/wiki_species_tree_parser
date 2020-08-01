package github.nea14e.wiki_species_tree_parser.models;

import java.util.ArrayList;
import java.util.List;
import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class Tree {

    @SerializedName("_id")
    @Expose
    public Object id;
    @SerializedName("levels")
    @Expose
    public List<Level> levels = new ArrayList<>();
    @SerializedName("translation")
    @Expose
    public Translation translation;
    @SerializedName("_language_key")
    @Expose
    public String languageKey;

    @Override
    public String toString() {
        return "Tree{" +
                "id=" + id +
                ", translation=" + translation +
                ", languageKey='" + languageKey + '\'' +
                '}';
    }
}
