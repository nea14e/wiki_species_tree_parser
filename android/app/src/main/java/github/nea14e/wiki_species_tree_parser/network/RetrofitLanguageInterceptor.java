package github.nea14e.wiki_species_tree_parser.network;

import android.os.Build;
import android.os.LocaleList;

import androidx.annotation.NonNull;

import java.io.IOException;
import java.util.Locale;

import okhttp3.Interceptor;
import okhttp3.Request;
import okhttp3.Response;

public class RetrofitLanguageInterceptor implements Interceptor {

    private String language;

    @NonNull
    @Override
    public Response intercept(Chain chain) throws IOException {
        Request originalRequest = chain.request();
        Request requestWithHeaders = originalRequest.newBuilder()
                .header("Accept-Language", getLanguage())
                .build();
        return chain.proceed(requestWithHeaders);
    }

    private String getLanguage() {
        if (this.language == null) {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.N) {
                this.language = LocaleList.getDefault().toLanguageTags();
            } else {
                this.language = Locale.getDefault().getLanguage();
            }
        }
        return this.language;
    }
}