package com.example.glassteach_filemanage;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;

import android.app.Activity;
import android.content.Intent;
import android.util.Log;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;

import com.google.android.glass.media.CameraManager;

import android.os.AsyncTask;
import android.provider.MediaStore;

public class LoadingMenuActivity extends Activity {
	@Override
    public void onAttachedToWindow() {
        super.onAttachedToWindow();
        openOptionsMenu();
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
    	Log.d("DEBUG", "Creating menu");
        MenuInflater inflater = getMenuInflater();
        inflater.inflate(R.menu.loading_menu, menu);
        return true;
    }
    
    @Override
    protected void onResume() {
    	super.onResume();
    	Log.d("DEBUG", "Resuming Menu");
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle item selection.
        switch (item.getItemId()) {
            case R.id.stop:
                stopService(new Intent(this, FileManageService.class));
                return true;
            case R.id.monitorOn:
            	startService(new Intent(this, MonitorOnService.class));
            	return true;
            case R.id.monitorOff:
            	startService(new Intent(this, MonitorOffService.class));
            	return true;
            case R.id.pushFile:
            	startActivityForResult(new Intent(this, FilePushActivity.class), 8081);
            	return true;
            case R.id.pullFile:
            	startActivityForResult(new Intent(this, FilePullActivity.class), 8082);
            	return true;
            case R.id.record:
            	startActivityForResult(new Intent(MediaStore.ACTION_VIDEO_CAPTURE), 8080);
            	
            default:
                return super.onOptionsItemSelected(item);
        }
    }
    
    @Override
    protected void onActivityResult (int requestCode, int resultCode, Intent data) {
    	Log.d("DEBUG", "requestCode: " + requestCode);
    	if (requestCode == 8080 && resultCode == RESULT_OK) {
    		//write video data to teacher
    		
    		Log.d("DEBUG", data.getStringExtra(CameraManager.EXTRA_VIDEO_FILE_PATH));
    		new VideoStore().execute(data.getStringExtra(CameraManager.EXTRA_VIDEO_FILE_PATH));
    	}
    	else if (requestCode == 8081 && resultCode == RESULT_OK) {
    		Log.d("DEBUG", "File Pushed Sucessfully");
    	}
    	
    	else if (requestCode == 8082 && resultCode == RESULT_OK) {
    		Log.d("DEBUG", "File Pulled Sucessfully");
    	}
    	
    	Log.d("DEBUG", "Closing menu");
    	finish();
    }
    
    class VideoStore extends AsyncTask<String, Void, Void> {

        protected Void doInBackground(String... file) {
        	
        	try {
    			Socket socket = new Socket("54.187.236.208", 8080);
    			Log.d("DEBUG", "Connected to socket");
    			PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
    			BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
    			//send glass ident
    			char nc = (char) 0x00;
    			out.print("glass" + nc + nc + nc + nc + nc);
    			String file_path = file[0];
    			String name = file_path.substring(file_path.lastIndexOf("/") + 1);
    			//initialize VideoStore protocol
    			String op = "video-store=" + name;
    			while (op.length() < 128) op = op + nc;
    			out.print(op);
    			out.flush();
    			//start writing the file in 2048 length packets
    			File video = new File(file_path);
    			BufferedReader videoIn = new BufferedReader(new FileReader(video));
    			char[] buffer = new char[2048];
    			int readCount = 0;
    			int nullCount = 0;
    			Log.d("DEBUG", "Starting to write video");
    			while ((readCount = videoIn.read(buffer, 0, 2048)) == 2048) {
    				for (int i = 0; i < readCount; i++) {
    					if (buffer[i] == nc) nullCount++;
    				}
    				out.print(new String(buffer));
    				out.flush();
    			}
    			Log.d("DEBUG", "Writing last packet, nullBytes: " + nullCount);
    			//pad the last buffer with null bytes
    			for (int i = readCount; i < 2048; i++) {
    				buffer[i] = nc;
    			}
    			out.print(new String(buffer));
    			out.flush();
    			//send a completely null packet
    			for (int i = 0; i < 2048; i++) {
    				buffer[i] = nc;
    			}
    			
    			out.print(new String(buffer));
    			out.flush();
    			
    			Log.d("DEBUG", "Finished writing Video");
    			out.close();
    			videoIn.close();
    			in.close();
    			
    		} catch (UnknownHostException e) {
    			// TODO Auto-generated catch block
    			e.printStackTrace();
    		} catch (IOException e) {
    			Log.d("DEBUG", "Unable to connect to socket");
    			e.printStackTrace();
    		} catch (Exception e) {
    			Log.d("DEBUG", "Exception!");
    			e.printStackTrace();
    		}
        	return null;
        }
    }
}
