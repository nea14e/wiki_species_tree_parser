package github.nea14e.wiki_species_tree_parser;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {

    TextView header_txt;
    TextView message_txt;
    Button go_btn;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        header_txt = findViewById(R.id.header_txt);
        message_txt = findViewById(R.id.message_txt);
        go_btn = findViewById(R.id.go_btn);

        go_btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                header_txt.setText(R.string.header_txt_success);

                StringBuilder sb = new StringBuilder();
                for (int i = 0; i < 100; ++i) {
                    sb.append(i).append(" ");
                }
                message_txt.setText(sb.toString());
            }
        });
    }
}