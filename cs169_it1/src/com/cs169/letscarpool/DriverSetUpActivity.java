package com.cs169.letscarpool;

import com.cs169.letscarpool.R;

import android.os.Bundle;
import android.app.Activity;
import android.view.View;
import android.widget.Button;

public class DriverSetUpActivity extends Activity{

	Button driverSetUpB;
	
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.driver_setup_view);
        
        driverSetUpB = (Button) findViewById(R.id.driver_setup);
        
        driverSetUpB.setOnClickListener(new View.OnClickListener() {
			
			@Override
			public void onClick(View v) {
				// TODO Auto-generated method stub
				
			}
		});
    }
}
