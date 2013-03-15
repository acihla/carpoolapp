package com.cs169.letscarpool;

import com.cs169.letscarpool.R;

import android.os.Bundle;
import android.app.Activity;
import android.view.View;
import android.widget.Button;

public class RiderSetUpActivity extends Activity {
	
	Button riderSetUpB;
	
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.rider_setup_view);
        
        riderSetUpB = (Button) findViewById(R.id.rider_setup);
        
        riderSetUpB.setOnClickListener(new View.OnClickListener() {
			
			@Override
			public void onClick(View v) {
				// TODO Auto-generated method stub
				
			}
		});
    }

}
