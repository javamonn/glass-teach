package com.example.glassteach_filemanage;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.ArrayList;
import java.util.Arrays;

import com.google.android.glass.app.Card;
import com.google.android.glass.widget.CardScrollAdapter;
import com.google.android.glass.widget.CardScrollView;

import android.app.Activity;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.RemoteViews;
import android.widget.AdapterView;

public class FilePushActivity extends Activity implements AdapterView.OnItemClickListener {
	
	ArrayList<Card> cards;
	ScrollAdapter scrollAdapter;
	CardScrollView scrollView;
	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		cards = new ArrayList<Card>();
		String[] files = ((Globals) (getApplicationContext())).systemFiles;
		Log.d("DEBUG", "system_state in file_push: " + Arrays.toString(files));
		for (int i = 0; i < files.length; i++) {
			String file = files[i];
			//file is a folder (which we currently skip)
			if (file.charAt(0) == (char) 0x02) {
				continue;
			}
			Card card = new Card(this);
			card.setText(files[i]);
			card.setFootnote("Push File to Student Computers");
			//TODO: add image based on file type
			cards.add(card);
		}
		scrollAdapter = new ScrollAdapter();
		scrollView = new CardScrollView(this);
		scrollView.setAdapter(scrollAdapter);
		scrollView.setOnItemClickListener(this);
		scrollView.activate();
		setContentView(scrollView);
	}
    
    @Override
	public void onItemClick(AdapterView<?> arg0, View arg1, int pos, long arg3) {
		// TODO Auto-generated method stub
    	Log.d("DEBUG", "Item clicked: " + cards.get(pos).getText());
    	String file = cards.get(pos).getText().toString();
    	new FilePush().execute(file);
    	finish();
	}
		
	private class ScrollAdapter extends CardScrollAdapter {

        @Override
        public int getPosition(Object item) {
            return cards.indexOf(item);
        }

        @Override
        public int getCount() {
            return cards.size();
        }

        @Override
        public Object getItem(int position) {
            return cards.get(position);
        }

        /**
         * Returns the amount of view types.
         */
        @Override
        public int getViewTypeCount() {
            return Card.getViewTypeCount();
        }

        /**
         * Returns the view type of this card so the system can figure out
         * if it can be recycled.
         */
        @Override
        public int getItemViewType(int position){
            return cards.get(position).getItemViewType();
        }

        @Override
        public View getView(int position, View convertView,
                ViewGroup parent) {
            return cards.get(position).getView(convertView, parent);
        }
    }
	
	class FilePush extends AsyncTask<String, Void, Void> {

        protected Void doInBackground(String... file) {
        	
        	try {
    			Socket socket = new Socket("54.187.236.208", 8080);
    			Log.d("DEBUG", "Connected to socket");
    			PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
    			BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
    			//send glass ident
    			char nc = (char) 0x00;
    			out.print("glass" + nc + nc + nc + nc + nc);
    			//initialize file-push protocol
    			String op = "file-push=" + file;
    			while (op.length() < 128) op = op + nc;
    			out.print(op);
    			out.flush();
    		} catch (UnknownHostException e) {
    			// TODO Auto-generated catch block
    			e.printStackTrace();
    		} catch (IOException e) {
    			Log.d("DEBUG", "Unable to connect to socket");
    			e.printStackTrace();
    		} catch (Exception e) {
    			Log.d("DEBUG", "Exception!");
    		}
        	return null;
        }
    }
}
