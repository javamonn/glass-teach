package com.example.glassteach_filemanage;

import android.app.Activity;
import android.content.Intent;
import android.util.Log;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;

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
            	startActivity(new Intent(this, FilePushActivity.class));
            	return true;
            case R.id.pullFile:
            	startActivity(new Intent(this, FilePullActivity.class));
            	return true;
            default:
                return super.onOptionsItemSelected(item);
        }
    }

    @Override
    public void onOptionsMenuClosed(Menu menu) {
        // Nothing else to do, closing the activity.
        finish();
    }

}
