package github.nea14e.wiki_species_tree_parser.network;

import android.content.Context;
import android.content.DialogInterface;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AlertDialog;
import androidx.core.content.ContextCompat;

import org.greenrobot.eventbus.EventBus;

import github.nea14e.wiki_species_tree_parser.MainActivity;
import github.nea14e.wiki_species_tree_parser.R;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

abstract public class SmartCallback<T> implements Callback<T> {

    private final boolean isLongOperation;

    public SmartCallback(boolean isLongOperation) {
        this.isLongOperation = isLongOperation;
        if (isLongOperation) {
            EventBus.getDefault().post(new MainActivity.StartLongOperationEvent());
        }
        EventBus.getDefault().post(new MainActivity.StartLongOperationEvent());
    }

    @Override
    public void onResponse(@NonNull Call<T> call, @NonNull Response<T> response) {
        if (this.isLongOperation) {
            EventBus.getDefault().post(new MainActivity.StopLongOperationEvent());
        }
        if (response.isSuccessful()) {
            onData(response.body());
        } else {
            final String message = response.message();
            EventBus.getDefault().post(new SmartCallback.OnNetworkErrorEvent(message));
        }
    }

    @Override
    public void onFailure(@NonNull Call<T> call, @NonNull Throwable t) {
        if (this.isLongOperation) {
            EventBus.getDefault().post(new MainActivity.StopLongOperationEvent());
        }
        String message = t.getLocalizedMessage();
        EventBus.getDefault().post(new SmartCallback.OnNetworkErrorEvent(message));
    }

    abstract protected void onData(T data);

    public static class OnNetworkErrorEvent {
        public final String message;

        private OnNetworkErrorEvent(String message) {
            this.message = message;
        }
    }
}
