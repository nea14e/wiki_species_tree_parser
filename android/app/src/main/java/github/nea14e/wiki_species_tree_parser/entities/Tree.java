package github.nea14e.wiki_species_tree_parser.entities;

import android.os.Parcel;
import android.os.Parcelable;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

import java.util.ArrayList;
import java.util.List;

public class Tree implements Parcelable {

    @Nullable
    @SerializedName("_id")
    @Expose
    public Long id;
    @SerializedName("levels")
    @Expose
    public List<Level> levels = new ArrayList<>();
    @SerializedName("translation")
    @Expose
    public Translation translation;
    @SerializedName("_language_key")
    @Expose
    public String languageKey;

    @NonNull
    @Override
    public String toString() {
        return "Tree{" +
                "id=" + id +
                ", translation=" + translation +
                ", languageKey='" + languageKey + '\'' +
                '}';
    }

    // Parcelable implementation

    public final static Parcelable.Creator<Tree> CREATOR = new Creator<Tree>() {
        public Tree createFromParcel(Parcel in) {
            return new Tree(in);
        }

        public Tree[] newArray(int size) {
            return (new Tree[size]);
        }
    };

    protected Tree(Parcel in) {
        this.id = ((Long) in.readValue((Long.class.getClassLoader())));
        in.readList(this.levels, (Level.class.getClassLoader()));
        this.translation = ((Translation) in.readValue((Translation.class.getClassLoader())));
        this.languageKey = in.readString();
    }

    public Tree() {
    }

    public void writeToParcel(Parcel dest, int flags) {
        dest.writeValue(id);
        dest.writeList(levels);
        dest.writeValue(translation);
        dest.writeValue(languageKey);
    }

    public int describeContents() {
        return 0;
    }

}
