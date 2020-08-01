package github.nea14e.wiki_species_tree_parser;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.content.ContextCompat;

import android.content.pm.PackageManager;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import github.nea14e.wiki_species_tree_parser.models.Check;
import github.nea14e.wiki_species_tree_parser.models.Tree;
import github.nea14e.wiki_species_tree_parser.network.RetrofitHelper;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class MainActivity extends AppCompatActivity {

    private TextView header_txt;
    private TextView message_txt;
    private Button go_btn;

    private RetrofitHelper retrofitHelper;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        header_txt = findViewById(R.id.header_txt);
        message_txt = findViewById(R.id.message_txt);
        go_btn = findViewById(R.id.go_btn);

        retrofitHelper = new RetrofitHelper();

        if (
                ContextCompat.checkSelfPermission(getApplicationContext(), "android.permission.INTERNET") !=
                        PackageManager.PERMISSION_GRANTED
        ) {
            header_txt.setText(R.string.header_txt_no_permission);
        }

        go_btn.setOnClickListener(view -> {
            header_txt.setText(R.string.header_txt_quering);

            Call<Tree> call = retrofitHelper.api.getTreeDefault();
            call.enqueue(new Callback<Tree>() {
                @Override
                public void onResponse(Call<Tree> call, Response<Tree> response) {
                    header_txt.setText(R.string.header_txt_success);
                    Tree answer = response.body();
                    message_txt.setText(answer.toString());
                }

                @Override
                public void onFailure(Call<Tree> call, Throwable t) {
                    header_txt.setText(R.string.header_txt_error);
                    message_txt.setText(t.getMessage());
                }
            });
        });
    }
}