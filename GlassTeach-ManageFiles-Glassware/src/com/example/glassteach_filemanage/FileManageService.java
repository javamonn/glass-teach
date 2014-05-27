package com.example.glassteach_filemanage;

import android.app.PendingIntent;
import android.app.Service;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.IBinder;
import android.util.Log;
import android.widget.RemoteViews;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.Arrays;

import com.google.android.glass.timeline.LiveCard;
import com.google.android.glass.timeline.LiveCard.PublishMode;


/**
 * Service to turn off all monitors connected to VPS
 */
public class FileManageService extends Service {

	//card displayed while first probing the network
	private LiveCard loadingLiveCard;
	
    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
    	Log.d("DEBUG", "start up service");
    	if (loadingLiveCard == null) {
    		loadingLiveCard = new LiveCard(this, "loading live card");
    		RemoteViews loadingView = new RemoteViews(this.getPackageName(), R.layout.loading_layout);
    		loadingLiveCard.setViews(loadingView);
    		loadingLiveCard.attach(this);
    		
    		Intent menuIntent = new Intent(this, LoadingMenuActivity.class);
    	    loadingLiveCard.setAction(PendingIntent.getActivity(this, 0, menuIntent, 0));
    		loadingLiveCard.publish(PublishMode.REVEAL);
    		Log.d("DEBUG", "Published loading live card");
    	} else {
    		loadingLiveCard.navigate();
    	}
    	new FileDir().execute();
        return START_STICKY;
    }

    @Override
    public void onDestroy() {
    	Log.d("DEBUG", "Destroying live card service");
    	loadingLiveCard.unpublish();
    	loadingLiveCard = null;
        super.onDestroy();
    }
    
    
    class FileDir extends AsyncTask<Void, Void, String[]> {

        protected String[] doInBackground(Void... urls) {
        	String[] output = new String[2];
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
    			String res = in.readLine();
    			String studentCount = res.substring(0, res.indexOf(new Character((char) 0x01).toString()));
    			res = res.substring(res.indexOf("=") + 1, res.indexOf(nc));
    			Log.d("DEBUG", "Student count: " + studentCount);
    			Log.d("DEBUG", "File-dir string: " + res);
    			in.close();
    			out.close();
    			output[0] = studentCount;
    			output[1] = res;
    		} catch (UnknownHostException e) {
    			// TODO Auto-generated catch block
    			e.printStackTrace();
    		} catch (IOException e) {
    			Log.d("DEBUG", "Unable to connect to socket");
    			e.printStackTrace();
    		} catch (Exception e) {
    			Log.d("DEBUG", "Exception!");
    		}
        	return output;
            
        }

        protected void onPostExecute(String[] output) {
        	if (output[0] != null) {
        		String[] files = output[1].split(new Character((char) 0x01).toString());
        		Log.d("DEBUG", "recieved data: " + Arrays.toString(files));
        		
        		RemoteViews loadingView = new RemoteViews(FileManageService.this.getPackageName(), R.layout.main_layout);
        		loadingView.setTextViewText(R.id.students_connected, output[0] + " Students In Class");
        		loadingLiveCard.setViews(loadingView);
        		
        		((Globals) (FileManageService.this.getApplicationContext())).systemFiles = files;
        		((Globals) (FileManageService.this.getApplicationContext())).connectedStudents = Integer.parseInt(output[0]);
        	} else {
        		Log.d("DEBUG", "Cant connect to server!");
        	}
        }
    }
}
