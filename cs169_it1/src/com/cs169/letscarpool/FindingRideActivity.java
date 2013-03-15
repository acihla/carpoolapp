package com.cs169.letscarpool;

import java.util.ArrayList;
import java.util.HashMap;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import com.cs169.letscarpool.R;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;

public class FindingRideActivity extends Activity {
	public static final String TAG = "PostingRideActivity";
	public static final String SearchRideURL="http://young-tor-7977.herokuapp.com//rider/search";
	Button findRideButton, mapMeButton;
	EditText date, timeDepart;
    String destLong, destLat, departLong, departLat;
	JSONObject retrievedObject;
	ListView resultList;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.finding_ride_view);

		findRideButton = (Button)findViewById(R.id.find_ride_button);
		mapMeButton = (Button)findViewById(R.id.map_button);
		date = (EditText)findViewById(R.id.date_content);
		timeDepart = (EditText)findViewById(R.id.time_depart_content);

		findRideButton.setOnClickListener(new View.OnClickListener() {

			@Override
			public void onClick(View v) {
				// TODO Auto-generated method stub
				retrievedObject = searchRide(date.getText().toString(), timeDepart.getText().toString(),
						"0", "0");

				//Change default error later
				if (retrievedObject!=null) {
					//String response = "{\"rides\": [{\"status\": \"False\", \"depart_time\": \"1992-04-17T05:00:00Z\", \"driver_info\": {\"car_mileage\": 13123, \"car_type\": \"Coupe\", \"license_no\": \"ABV32C\", \"driver\": {\"username\": \"pjlee\", \"cellphone\": \"510-910-2613\", \"firstname\": \"first\", \"dob\": \"1990-03-15\", \"lastname\": \"last\", \"avg_rating\": 3.0, \"driverOrRider\": \"rider\", \"comments\": \"hihih hihi comments\", \"password\": \"asdf\", \"email\": \"nadapeter@gmail.com\"}, \"car_make\": \"Toyota\", \"license_exp\": \"2016-01-11\", \"max_passengers\": 4}, \"maps_info\": \" yo\"}";	
					
					//display the routes sent from the server
					JSONArray rides = new JSONArray();
					JSONObject ride, driver_info, driver;

					int numRoutes;
					int status;
					ArrayList<HashMap<String, String>> routes = new ArrayList<HashMap<String,String>>();
					HashMap<String, String> route;

					try {
						status = retrievedObject.getInt("errCode");
						if (status==1){
							numRoutes = retrievedObject.getInt("size");
							rides = retrievedObject.getJSONArray("rides");

							for (int i = 0; i < numRoutes; i++) {
								ride = rides.getJSONObject(i);
								route = new HashMap<String, String>(22);
								route.put("map_info", ride.getString("maps_info"));
								driver_info = ride.getJSONObject("driver_info");
								driver = driver_info.getJSONObject("driver");
								route.put("car_mileage", driver_info.getString("car_mileage"));
								route.put("license_no", driver_info.getString("license_no"));
								route.put("car_type", driver_info.getString("car_type"));
								//
								route.put("username", driver.getString("username"));
								route.put("cellphone", driver.getString("cellphone"));
								//route.put("password", driver.getString("password"));
								route.put("firstname", driver.getString("firstname"));
								route.put("dob", driver.getString("dob"));
								route.put("lastname", driver.getString("lastname"));
								route.put("avg_rating", driver.getString("avg_rating"));
								route.put("comments", driver.getString("comments"));
								route.put("email", driver.getString("email"));
								route.put("sex", driver.getString("sex"));
								//
								route.put("car_make", driver_info.getString("car_make"));
								route.put("license_exp", driver_info.getString("license_exp"));
								route.put("max_passengers", driver_info.getString("max_passengers"));
								route.put("depart_time", ride.getString("depart_time"));
								routes.add(route);
							
								displayRoutes(routes);
							}
						}
						else{
							//Error Do something
						}
					} catch (JSONException e) {
						// TODO Auto-generated catch block
						Log.d(TAG,e.getMessage());
					} catch (Exception e) {
						// TODO Auto-generated catch block
						Log.d(TAG,e.getMessage());
					}
				} else {
					//
				}
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

private JSONObject searchRide(String date, String timedepart, String lat, String longitude){
	JSONObject obj = new JSONObject();
	try{
		Log.d(TAG,"Search Ride: date="+date+" time-depart="+timedepart+" lat="+lat+" long="+longitude);
		JSONObject postData = new JSONObject();
		JSONObject locData = new JSONObject();
		locData.put("lat", lat);
		locData.put("long", longitude);
		postData.put("date", date);
		postData.put("time-depart", timedepart);
		postData.put("depart-loc", locData.toString());
		Log.d(TAG,"postData created");
		obj = HTTPClient.sendHttpPost(SearchRideURL, postData);
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

	private void displayRoutes(ArrayList<HashMap<String,String>> routes){
        setContentView(R.layout.show_result_list);
        resultList = (ListView) findViewById(R.id.ResultList);
        
        ArrayList<SearchResultDetails> details = new ArrayList<SearchResultDetails>();
        for(int i=0; i<routes.size(); i++){
            SearchResultDetails Detail;
            Detail = new SearchResultDetails();
            Detail.setIcon(R.drawable.ic_launcher);
            Detail.setUsername(routes.get(i).get("username"));
            Detail.setMapInfo(routes.get(i).get("map_info"));
            Detail.setDepartTime(routes.get(i).get("depart_time"));
            Detail.setAverageRating(routes.get(i).get("avg_rating"));
            details.add(Detail);
        }
        
        resultList.setAdapter(new CustomAdapter(details , this));
            
	}

}
