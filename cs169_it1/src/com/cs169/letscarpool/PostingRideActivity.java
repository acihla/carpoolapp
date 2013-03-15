package com.cs169.letscarpool;

import org.json.JSONException;
import org.json.JSONObject;

import com.cs169.letscarpool.R;

import android.os.Bundle;
import android.app.Activity;
import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

public class PostingRideActivity extends Activity{
	public static final String TAG = "PostingRideActivity";
	public static final String PostRideURL="http://young-tor-7977.herokuapp.com//driver/addroute";
	Button postRideButton, mapMeButton;
	EditText date, timeDepart, carMake, carModel, carMileage, maxPassengers;
	String destLong, destLat, departLong, departLat;
	JSONObject retrievedObject;

	private static final int SUCCESS = 1;// a success
	private static final int ERR_BAD_DEPARTURE = -1; //Departure location is not valid
	private static final int ERR_BAD_DESTINATION = -2; // Destination location is not valid
	private static final int ERR_BAD_USERID = -3; // UID does not exist in db, or is not a driver
	private static final int ERR_BAD_TIME = -4; //format for time is bad
	private static final int ERR_DATABASE_SEARCH_ERROR = -5; 
	private static final int ERR_BAD_HEADER= -6;
	private static final int ERR_BAD_SERVER_RESPONSE = -7;
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.posting_ride_view);

		postRideButton = (Button)findViewById(R.id.post_ride_button);
		timeDepart = (EditText)findViewById(R.id.time_depart_content);
		mapMeButton = (Button)findViewById(R.id.map_button);


		//Change so that it is disabled until Map Me is pressed
		postRideButton.setOnClickListener(new View.OnClickListener() {

			@Override
			public void onClick(View v) {
				// TODO Auto-generated method stub
				retrievedObject = postRide(1, timeDepart.getText().toString(),
						departLat, departLong, destLat, destLong);
				String dialogMessage="";

				//Change default error later
				try {
					switch(retrievedObject.getInt("errCode")){
					case SUCCESS:
						dialogMessage = "Ride successfully added!";
						break;
					case ERR_BAD_DEPARTURE:
						dialogMessage = "Sorry, bad departure. Please try again.";
						break;
					case ERR_BAD_DESTINATION:
						dialogMessage = "Sorry, bad destination. Please try again.";
						break;
					case ERR_BAD_USERID:
						dialogMessage = "Sorry, bad user ID. Please try again.";
						break;
					case ERR_BAD_TIME:
						dialogMessage = "Sorry, bad time. Please try again.";
						break;
					case ERR_DATABASE_SEARCH_ERROR:
						dialogMessage = "Sorry, bad database search. Please try again.";
						break;
					case ERR_BAD_HEADER:
						dialogMessage = "Sorry, bad header. Please try again.";
						break;
					case ERR_BAD_SERVER_RESPONSE:
						dialogMessage = "Sorry, bad server response. Please try again.";
						break;

					}
				} catch (JSONException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
				
				Log.d(TAG, "Dialog Message: "+dialogMessage);
				AlertDialog.Builder adb= new AlertDialog.Builder(PostingRideActivity.this);
				adb.setMessage(dialogMessage);
				adb.setPositiveButton("OK", new AlertDialog.OnClickListener(){

					@Override
					public void onClick(DialogInterface dialog, int which) {
						// TODO Auto-generated method stub
						finish();
					}

				});
				adb.show();
			}
		});

		mapMeButton.setOnClickListener(new View.OnClickListener() {

			@Override
			public void onClick(View v) {
				// TODO Auto-generated method stub
				Intent launchMapIntent = new Intent(getBaseContext(), MapViewActivity.class);
				launchMapIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
				startActivityForResult(launchMapIntent, 1);
			}

		});


	}
	@Override
	protected void onActivityResult(int requestCode, int resultCode, Intent data){
		if (requestCode==1){
			if (resultCode == RESULT_OK){
				destLong = data.getStringExtra("destLong");
				destLat = data.getStringExtra("destLat");
				departLong = data.getStringExtra("departLong");
				departLat = data.getStringExtra("departLat");
			}
			if (resultCode == RESULT_CANCELED){
				//No result Returned
				destLong = "0";
				destLat = "0";
				departLong = "0";
				departLat = "0";

			}
		}

	}

	public JSONObject postRide(int userID, String timedepart, String departlat, String departlong,
			String destlat, String destlong){
		JSONObject obj = new JSONObject();
		try{
			Log.d(TAG,"Post Ride: date="+date+" time-depart="+timedepart);
			JSONObject postData = new JSONObject();
			JSONObject departData = new JSONObject();
			JSONObject destData = new JSONObject();
			//JSON Object to be sent
			postData.put("user", userID);
			postData.put("edt", timedepart);
			postData.put("depart-lat", departlat);
			postData.put("depart-long", departlong);
			postData.put("dest-lat", destlat);
			postData.put("dest-long", destlong);
			Log.d(TAG,"postData created");
			//Send and retrieve JSON from server
			obj = HTTPClient.sendHttpPost(PostRideURL, postData);
			Log.d(TAG,"Retrieved obj");
		}

		catch (JSONException e) {
			// TODO Auto-generated catch block
			Log.d(TAG,e.getMessage());
		}
		catch (Exception e) {
			// TODO Auto-generated catch block
			Log.d(TAG,e.getMessage());
		}


		return obj;

	}



}
