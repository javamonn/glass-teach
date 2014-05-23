package com.example.glassteach_monitoron;

import android.app.Service;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.IBinder;
import android.util.Log;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;


/**
 * Service to turn off all monitors connected to VPS
 */
public class MonitorOnService extends Service {

    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
    	Log.d("Debug", "start up glass");
    	new Connect().execute();
        return START_STICKY;
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
    }
    
    
    class Connect extends AsyncTask<Void, Void, Void> {

        protected Void doInBackground(Void... urls) {
        	try {
    			Socket socket = new Socket("54.187.236.208", 8080);
    			Log.d("DEBUG", "Connected to socket");
    			PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
    			BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
    			//send glass ident
    			char nc = (char) 0x00;
    			out.println("glass" + nc + nc + nc + nc + nc);
    			String op = "monitor=on";
    			while (op.length() < 128) op = op + nc;
    			out.print(op);
    			out.flush();
    			out.close();
    		} catch (UnknownHostException e) {
    			// TODO Auto-generated catch block
    			e.printStackTrace();
    		} catch (IOException e) {
    			Log.d("DEBUG", "Unable to connect to socket");
    			e.printStackTrace();
    		}
        	return null;
            
        }

        protected void onPostExecute() {
        	stopSelf();
        }
    }
}
