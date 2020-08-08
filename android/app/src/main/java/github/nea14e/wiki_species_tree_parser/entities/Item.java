package github.nea14e.wiki_species_tree_parser.entities;

import android.os.Parcel;
import android.os.Parcelable;

import androidx.annotation.Nullable;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class Item implements Parcelable {

    @SerializedName("id")
    @Expose
    public long id;
    @SerializedName("page_url")
    @Expose
    public String pageUrl;
    @Nullable
    @SerializedName("image_url")
    @Expose
    public String imageUrl;
    @Nullable
    @SerializedName("parent_id")
    @Expose
    public Long parentId;
    @SerializedName("is_expanded")
    @Expose
    public boolean isExpanded;
    @SerializedName("is_selected")
    @Expose
    public boolean isSelected;
    @Nullable
    @SerializedName("leaves_count")
    @Expose
    public Long leavesCount;
    @SerializedName("title_for_language")
    @Expose
    public String titleForLanguage;
    @SerializedName("wiki_url_for_language")
    @Expose
    public String wikiUrlForLanguage;

    // Parcelable implementation

    public final static Parcelable.Creator<Item> CREATOR = new Creator<Item>() {
        public Item createFromParcel(Parcel in) {
            return new Item(in);
        }

        public Item[] newArray(int size) {
            return (new Item[size]);
        }
    };

    protected Item(Parcel in) {
        this.id = in.readLong();
        this.pageUrl = in.readString();
        this.imageUrl = in.readString();
        this.parentId = ((Long) in.readValue((Long.class.getClassLoader())));
        this.isExpanded = ((boolean) in.readValue((boolean.class.getClassLoader())));
        this.isSelected = ((boolean) in.readValue((boolean.class.getClassLoader())));
        this.leavesCount = ((Long) in.readValue((Long.class.getClassLoader())));
        this.titleForLanguage = in.readString();
        this.wikiUrlForLanguage = in.readString();
    }

    public Item() {
    }

    public void writeToParcel(Parcel dest, int flags) {
        dest.writeValue(id);
        dest.writeValue(pageUrl);
        dest.writeValue(imageUrl);
        dest.writeValue(parentId);
        dest.writeValue(isExpanded);
        dest.writeValue(isSelected);
        dest.writeValue(leavesCount);
        dest.writeValue(titleForLanguage);
        dest.writeValue(wikiUrlForLanguage);
    }

    public int describeContents() {
        return 0;
    }
}
