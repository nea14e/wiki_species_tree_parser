package github.nea14e.wiki_species_tree_parser.entities;

import android.os.Parcel;
import android.os.Parcelable;

import androidx.annotation.Nullable;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

import java.util.List;

public class Level implements Parcelable {

    @SerializedName("type")
    @Expose
    public String type;
    @SerializedName("items")
    @Expose
    public List<Item> items;
    @SerializedName("title_on_language")
    @Expose
    public String titleOnLanguage;
    @Nullable
    @SerializedName("level_parent_title")
    @Expose
    public String levelParentTitle;
    @SerializedName("is_level_has_selected_item")
    @Expose
    public boolean isLevelHasSelectedItem;

    // Parcelable implementation

    public final static Parcelable.Creator<Level> CREATOR = new Creator<Level>() {

        public Level createFromParcel(Parcel in) {
            return new Level(in);
        }

        public Level[] newArray(int size) {
            return (new Level[size]);
        }

    };

    protected Level(Parcel in) {
        this.type = ((String) in.readValue((String.class.getClassLoader())));
        in.readList(this.items, (Item.class.getClassLoader()));
        this.titleOnLanguage = ((String) in.readValue((String.class.getClassLoader())));
        this.levelParentTitle = ((String) in.readValue((String.class.getClassLoader())));
        this.isLevelHasSelectedItem = ((boolean) in.readValue((boolean.class.getClassLoader())));
    }

    public Level() {
    }

    public void writeToParcel(Parcel dest, int flags) {
        dest.writeValue(type);
        dest.writeList(items);
        dest.writeValue(titleOnLanguage);
        dest.writeValue(levelParentTitle);
        dest.writeValue(isLevelHasSelectedItem);
    }

    public int describeContents() {
        return 0;
    }
}
