package com.cs169.letscarpool;

import com.cs169.letscarpool.R;

import android.os.Bundle;
import android.app.Activity;
import android.view.View;
import android.widget.Button;

public class ProfileActivity extends Activity {
	Button requestB, routeB, rendezvousB;
	
	@Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.user_profile_view);
        
        requestB = (Button) findViewById(R.id.pending_requests);
        routeB = (Button) findViewById(R.id.published_routes);
        rendezvousB = (Button) findViewById(R.id.scheduled_rendezvous);
        
        requestB.setOnClickListener(new View.OnClickListener() {
			
			@Override
			public void onClick(View v) {
				// TODO Auto-generated method stub
				
			}
		});
        
        routeB.setOnClickListener(new View.OnClickListener() {
			
			@Override
			public void onClick(View v) {
				// TODO Auto-generated method stub
				
			}
		});
        
        rendezvousB.setOnClickListener(new View.OnClickListener() {
			
			@Override
			public void onClick(View v) {
				// TODO Auto-generated method stub
				
			}
		});
	}
}
