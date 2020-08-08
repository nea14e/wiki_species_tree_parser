package github.nea14e.wiki_species_tree_parser.models;

import android.os.Parcel;
import android.os.Parcelable;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class Item implements Parcelable {

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
        this.id = ((Long) in.readValue((Long.class.getClassLoader())));
        this.pageUrl = ((String) in.readValue((String.class.getClassLoader())));
        this.imageUrl = ((String) in.readValue((String.class.getClassLoader())));
        this.parentId = ((Long) in.readValue((Long.class.getClassLoader())));
        this.isExpanded = ((Boolean) in.readValue((Boolean.class.getClassLoader())));
        this.isSelected = ((Boolean) in.readValue((Boolean.class.getClassLoader())));
        this.leavesCount = ((Long) in.readValue((Long.class.getClassLoader())));
        this.titleForLanguage = ((String) in.readValue((String.class.getClassLoader())));
        this.wikiUrlForLanguage = ((String) in.readValue((String.class.getClassLoader())));
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
