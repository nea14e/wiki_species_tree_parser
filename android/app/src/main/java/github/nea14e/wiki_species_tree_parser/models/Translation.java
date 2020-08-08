package github.nea14e.wiki_species_tree_parser.models;

import android.os.Parcel;
import android.os.Parcelable;

import androidx.annotation.NonNull;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class Translation implements Parcelable {

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

    @NonNull
    @Override
    public String toString() {
        return "Translation{" +
                "comment='" + comment + '\'' +
                ", langKey='" + langKey + '\'' +
                '}';
    }

    // Parcelable implementation

    public final static Parcelable.Creator<Translation> CREATOR = new Creator<Translation>() {


        public Translation createFromParcel(Parcel in) {
            return new Translation(in);
        }

        public Translation[] newArray(int size) {
            return (new Translation[size]);
        }

    }
            ;

    protected Translation(Parcel in) {
        this.comment = ((String) in.readValue((String.class.getClassLoader())));
        this.langKey = ((String) in.readValue((String.class.getClassLoader())));
        this.rankWord = ((String) in.readValue((String.class.getClassLoader())));
        this.siteTitle = ((String) in.readValue((String.class.getClassLoader())));
        this.parentWord = ((String) in.readValue((String.class.getClassLoader())));
        this.searchWord = ((String) in.readValue((String.class.getClassLoader())));
        this.authorsWord = ((String) in.readValue((String.class.getClassLoader())));
        this.authorsContent = ((String) in.readValue((String.class.getClassLoader())));
        this.siteDescription = ((String) in.readValue((String.class.getClassLoader())));
        this.tipOfTheDayWord = ((String) in.readValue((String.class.getClassLoader())));
    }

    public Translation() {
    }

    public void writeToParcel(Parcel dest, int flags) {
        dest.writeValue(comment);
        dest.writeValue(langKey);
        dest.writeValue(rankWord);
        dest.writeValue(siteTitle);
        dest.writeValue(parentWord);
        dest.writeValue(searchWord);
        dest.writeValue(authorsWord);
        dest.writeValue(authorsContent);
        dest.writeValue(siteDescription);
        dest.writeValue(tipOfTheDayWord);
    }

    public int describeContents() {
        return 0;
    }
}