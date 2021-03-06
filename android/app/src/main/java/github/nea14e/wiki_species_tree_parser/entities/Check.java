package github.nea14e.wiki_species_tree_parser.entities;

import androidx.annotation.NonNull;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class Check {

    @SerializedName("title")
    @Expose
    public String title;
    @SerializedName("django_state")
    @Expose
    public String djangoState;
    @SerializedName("db_state")
    @Expose
    public String dbState;
    @SerializedName("info")
    @Expose
    public String info;
    @SerializedName("all_is_ok")
    @Expose
    public boolean allIsOk;

    @NonNull
    @Override
    public String toString() {
        return "title: " + title +
                "\ndjango_state: " + djangoState +
                "\ndb_state: " + dbState +
                "\ninfo: " + info +
                "\nall_is_ok: " + allIsOk;
    }

}