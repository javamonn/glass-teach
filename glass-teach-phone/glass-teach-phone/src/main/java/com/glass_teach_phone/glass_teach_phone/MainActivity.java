package com.glass_teach_phone.glass_teach_phone;

import android.app.Activity;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;

public class MainActivity extends Activity implements View.OnClickListener {

    Button monitor;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        monitor = (Button) findViewById(R.id.monitor);
        monitor.setOnClickListener(this);
    }

    @Override
    public void onClick(View view) {
        switch (view.getId()) {
            // turn monitor on and off
            case R.id.monitor:
                if (view.getTag().equals("on")) {
                    //send turn off command to computer
                    view.setTag("off");
                } else {
                    //send turn on command to host computer
                    view.setTag("on");
                }
        }
    }
}
