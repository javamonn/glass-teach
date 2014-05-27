package com.example.glassteach_filepush;

import android.app.Activity;
import android.app.Service;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.IBinder;
import android.util.Log;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;

import com.google.android.glass.app.Card;


/**
 * Service to push a selected file to student computers
 * 
 * TODO: stopSelf() to stop service somewhere
 */
public class FilePushActivity extends Activity {

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		Log.d("DEBUG", "creating activity");
		setContentView(R.layout.loading_layout);

		/*//display loading card
		Log.d("DEBUG", "creating activity");
		Card c = new Card(this);
		c.setText("Hello world");
		setContentView(c.getView());*/
		
		
	}  
    
    class Connect extends AsyncTask<Void, Void, String> {

        protected String doInBackground(Void... urls) {
        	String res = "";
        	try {
    			Socket socket = new Socket("54.187.236.208", 8080);
    			Log.d("DEBUG", "Connected to socket");
    			PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
    			BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
    			//send glass ident
    			char nc = (char) 0x00;
    			out.print("glass" + nc + nc + nc + nc + nc);
    			//initialize file-dir protocol
    			String op = "file-dir";
    			while (op.length() < 128) op = op + nc;
    			out.print(op);
    			out.flush();
    			//process response to display to user
    			res = in.readLine();
    			res = res.substring(res.indexOf("=") + 1, res.indexOf(nc));
    			Log.d("DEBUG", "File-dir string: " + res);
    			in.close();
    			out.close();
    		} catch (UnknownHostException e) {
    			// TODO Auto-generated catch block
    			e.printStackTrace();
    		} catch (IOException e) {
    			Log.d("DEBUG", "Unable to connect to socket");
    			e.printStackTrace();
    		} catch (Exception e) {
    			Log.d("DEBUG", "Exception!");
    		}
        	return res;
            
        }

        protected void onPostExecute(String res) {
        	String[] files = res.split(new Character((char) 0x01).toString());
        }
    }
}
