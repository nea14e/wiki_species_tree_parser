package github.nea14e.wiki_species_tree_parser.entities;

import android.os.Parcel;
import android.os.Parcelable;

import androidx.annotation.Nullable;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class SearchItem implements Parcelable {

    @SerializedName("id")
    @Expose
    public long id;
    @Nullable
    @SerializedName("rank_for_language")
    @Expose
    public String rankForLanguage;
    @SerializedName("title_for_language")
    @Expose
    public String titleForLanguage;
    @Nullable
    @SerializedName("image_url")
    @Expose
    public String imageUrl;
    @Nullable
    @SerializedName("rank_order")
    @Expose
    public Long rankOrder;
    @Nullable
    @SerializedName("leaves_count")
    @Expose
    public Long leavesCount;

    // Parcelable implementation

    public final static Parcelable.Creator<SearchItem> CREATOR = new Creator<SearchItem>() {

        public SearchItem createFromParcel(Parcel in) {
            return new SearchItem(in);
        }

        public SearchItem[] newArray(int size) {
            return (new SearchItem[size]);
        }

    }
            ;

    protected SearchItem(Parcel in) {
        this.id = in.readLong();
        this.rankForLanguage = in.readString();
        this.titleForLanguage = in.readString();
        this.imageUrl = in.readString();
        this.rankOrder = ((Long) in.readValue((Long.class.getClassLoader())));
        this.leavesCount = ((Long) in.readValue((Long.class.getClassLoader())));
    }

    public SearchItem() {
    }

    public void writeToParcel(Parcel dest, int flags) {
        dest.writeValue(id);
        dest.writeValue(rankForLanguage);
        dest.writeValue(titleForLanguage);
        dest.writeValue(imageUrl);
        dest.writeValue(rankOrder);
        dest.writeValue(leavesCount);
    }

    public int describeContents() {
        return 0;
    }
}