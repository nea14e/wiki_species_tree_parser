package github.nea14e.wiki_species_tree_parser.models;

import android.os.Parcel;
import android.os.Parcelable;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class TipOfTheDay implements Parcelable
{

    @SerializedName("id")
    @Expose
    public Long id;
    @SerializedName("tip_text")
    @Expose
    public String tipText;
    @SerializedName("species_id")
    @Expose
    public Long speciesId;
    @SerializedName("image_url")
    @Expose
    public String imageUrl;

    // Parcelable implementation

    public final static Parcelable.Creator<TipOfTheDay> CREATOR = new Creator<TipOfTheDay>() {

        public TipOfTheDay createFromParcel(Parcel in) {
            return new TipOfTheDay(in);
        }

        public TipOfTheDay[] newArray(int size) {
            return (new TipOfTheDay[size]);
        }

    }
            ;

    protected TipOfTheDay(Parcel in) {
        this.id = ((Long) in.readValue((Long.class.getClassLoader())));
        this.tipText = ((String) in.readValue((String.class.getClassLoader())));
        this.speciesId = ((Long) in.readValue((Long.class.getClassLoader())));
        this.imageUrl = ((String) in.readValue((String.class.getClassLoader())));
    }

    public TipOfTheDay() {
    }

    public void writeToParcel(Parcel dest, int flags) {
        dest.writeValue(id);
        dest.writeValue(tipText);
        dest.writeValue(speciesId);
        dest.writeValue(imageUrl);
    }

    public int describeContents() {
        return 0;
    }

}
