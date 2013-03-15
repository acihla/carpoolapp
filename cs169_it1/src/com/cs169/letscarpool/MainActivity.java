package com.cs169.letscarpool;

import com.cs169.letscarpool.R;

import android.os.Bundle;
import android.app.Activity;
import android.content.Intent;
import android.view.Menu;
import android.view.View;
import android.widget.Button;

public class MainActivity extends Activity {

	Button driverViewB, riderViewB, profileViewB;
	
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        driverViewB = (Button) findViewById(R.id.driver_view);
        riderViewB = (Button) findViewById(R.id.rider_view);
        profileViewB = (Button) findViewById(R.id.profile_view);
        
        driverViewB.setOnClickListener(new View.OnClickListener() {
			
			@Override
			public void onClick(View v) {
				// TODO Auto-generated method stub
				Intent launchPostRideIntent = new Intent(getBaseContext(), PostingRideActivity.class);
				launchPostRideIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
				getBaseContext().startActivity(launchPostRideIntent);
				
			}
		});
        
        riderViewB.setOnClickListener(new View.OnClickListener() {
			
			@Override
			public void onClick(View v) {
				// TODO Auto-generated method stub
				Intent launchFindRideIntent = new Intent(getBaseContext(), FindingRideActivity.class);
				launchFindRideIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
				getBaseContext().startActivity(launchFindRideIntent);
			}
		});
        
        profileViewB.setOnClickListener(new View.OnClickListener() {
			
			@Override
			public void onClick(View v) {
				// TODO Auto-generated method stub
				
			}
		});
        
        
    }


    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.main, menu);
        return true;
    }
    
}
