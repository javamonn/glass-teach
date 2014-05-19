package com.glass_teach_phone.glass_teach_phone;

import android.annotation.TargetApi;
import android.app.Activity;
import android.os.AsyncTask;
import android.os.Build;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.ProgressBar;
import android.widget.TextView;

import java.io.IOException;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.Scanner;

public class MainActivity extends Activity implements View.OnClickListener {

    Button monitorButton;
    ProgressBar progressBar;
    TextView helpText;
    TextView connectText;

    ServerSocket serverSocket;
    Socket socket;

    //to computer
    PrintWriter outStream;
    //from computer
    Scanner inStream;

    @TargetApi(Build.VERSION_CODES.CUPCAKE)
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        progressBar = (ProgressBar) findViewById(R.id.spinner);
        helpText = (TextView) findViewById(R.id.help_text);
        connectText = (TextView) findViewById(R.id.connect_text);
        monitorButton = (Button) findViewById(R.id.monitor);
        monitorButton.setOnClickListener(this);

        //attempt to connect

        Connect task = new Connect();
        task.execute();
    }

    @Override
    public void onClick(View view) {
        switch (view.getId()) {
            // turn monitor on and off
            case R.id.monitor:
                if (view.getTag().equals("on")) {
                    //send turn off command to computer
                    Log.d("DEBUG", "monitor off sent");
                    view.setTag("off");
                    outStream.println("monitor off");
                    monitorButton.setText("Turn On Monitor");
                } else {
                    //send turn on command to host computer
                    Log.d("DEBUG", "monitor on sent");
                    view.setTag("on");
                    outStream.println("monitor on");
                    monitorButton.setText("Turn off Monitor");
                }
        }
    }

    private class Connect extends AsyncTask<Void, Void, Void> {

        @Override
        protected Void doInBackground(Void... voids) {
            try {
                //port 38300 (arbitrary)
                serverSocket = new ServerSocket(38300);
                serverSocket.setSoTimeout(0);
                // attempt to connect, infinite time out
                Log.d("CONNECT", "Accepting connections");
                socket = serverSocket.accept();
                Log.d("CONECT", "Connection accepted");
                // get streams
                outStream = new PrintWriter(socket.getOutputStream(), true);
                inStream = new Scanner(socket.getInputStream());

            } catch (IOException e) {
                e.printStackTrace();
            }
            return null;
        }

        @Override
        public void onPostExecute(Void voids) {
            //if we reach here a connection has been established so we update UI
            helpText.setVisibility(View.GONE);
            connectText.setVisibility(View.GONE);
            progressBar.setVisibility(View.GONE);
            monitorButton.setVisibility(View.VISIBLE);
            //set connection flag so main UI knows we're ready

            //send message to computer so it knows we're connected


        }
    }
}
