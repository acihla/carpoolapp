package com.cs169.letscarpool;

import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.location.Address;
import android.location.Geocoder;
import android.os.AsyncTask;
import android.os.Bundle;
import android.graphics.Color;
import android.view.Menu;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;
import android.support.v4.app.FragmentActivity;
import android.util.Log;

import com.cs169.letscarpool.R;
import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.GoogleMap.OnMapClickListener;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.MarkerOptions;
import com.google.android.gms.maps.model.PolylineOptions;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

public class MapViewActivity extends FragmentActivity implements OnMapClickListener {
    // private static final LatLng SODA = new LatLng(37.875641,-122.258742);
    private GoogleMap mMap;
    private LatLng departLoc = null, destLoc = null;
    private int locCount;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.map_view);
        locCount = 0;
        
        // Location field and find button
        Button btn_find = (Button) findViewById(R.id.btn_find);
        View.OnClickListener btn_findListener = new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                EditText enterLoc = (EditText) findViewById(R.id.enter_loc);
                String loc = enterLoc.getText().toString();
                if (loc != null && !loc.equals("")) {
                    new GeocoderTask().execute(loc);
                }
            }
        };
        btn_find.setOnClickListener(btn_findListener);
        
        // Try to obtain the map from the SupportMapFragment.
        SupportMapFragment supMapFrag = (SupportMapFragment) getSupportFragmentManager().findFragmentById(R.id.map);
        mMap = supMapFrag.getMap();
        mMap.setOnMapClickListener(this);
    }
    
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.main, menu);
        return true;
    }
    
    /* Functions related to the find box */
    private class GeocoderTask extends AsyncTask<String, Void, List<Address>> {
        @Override
        protected List<Address> doInBackground(String... locName) {
            Geocoder geocoder = new Geocoder(getBaseContext());
            List<Address> addr = null;
            
            try {
                addr = geocoder.getFromLocationName(locName[0], 3);
            } catch (IOException e) {
                e.printStackTrace();
            }
            
            return addr;
        }
        
        @Override
        protected void onPostExecute(List<Address> addrs) {
            if (addrs == null || addrs.size() == 0) {
                Toast.makeText(getBaseContext(), "Location not found", Toast.LENGTH_SHORT).show();
            }
            // TODO: need to filter the list of addrs instead of getting the index 0
            Address addr = (Address) addrs.get(0);
            LatLng temp = new LatLng(addr.getLatitude(), addr.getLongitude());
            mMap.animateCamera(CameraUpdateFactory.newLatLng(temp));
            dropMarker(temp);
        }
    }

    /* Functions related to the MapFragment */
    @Override
    public void onMapClick(LatLng pos) {    
        dropMarker(pos);
    }
    
    private void dropMarker(LatLng pos) {
        switch (locCount) {
        case 0: // dropping the 1st pin - depart location
                departLoc = pos;
                mMap.addMarker(new MarkerOptions().position(departLoc).title("Departure Location"));
                locCount++;
                break;
                
        case 1: // dropping the 2nd pin - destination location
                destLoc = pos;
                mMap.addMarker(new MarkerOptions().position(destLoc).title("Destination Location"));
                locCount++;
                // generate route
                String url = getRouteURL(departLoc, destLoc);
                DrawTask drawTask = new DrawTask();
                drawTask.execute(url);
                break;
                
        case 2: // route confirmation
                AlertDialog.Builder adb = new AlertDialog.Builder(this);
                adb.setMessage("Please confirm route");
                adb.setNegativeButton("Cancel", null);
                adb.setPositiveButton("Confirm", new AlertDialog.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        Intent returnIntent=new Intent();
                        returnIntent.putExtra("departLong", Double.toString(departLoc.longitude));
                        returnIntent.putExtra("departLat", Double.toString(departLoc.latitude));
                        returnIntent.putExtra("destLong", Double.toString(destLoc.longitude));
                        returnIntent.putExtra("destLat", Double.toString(destLoc.latitude));
                        setResult(RESULT_OK, returnIntent);
                        finish();
                    }
                });
                adb.show();
                break;
        }
    }
    
    private String getRouteURL(LatLng departLoc, LatLng destLoc) {
        StringBuilder url = new StringBuilder();
        // base url
        url.append("http://maps.googleapis.com/maps/api/directions/");
        
        // response message type
        url.append("json");
        
        // departLoc info
        url.append("?origin=");
        url.append(Double.toString(departLoc.latitude));
        url.append(",");
        url.append(Double.toString(departLoc.longitude));
        
        // destLoc info
        url.append("&destination=");
        url.append(Double.toString(destLoc.latitude));
        url.append(",");
        url.append(Double.toString(destLoc.longitude));
        
        // other parameters
        url.append("&sensor=false");
        // url.append("&mode=driving");
        // url.append("&alternatives=true");
        
        return url.toString();
    }
    
    public void drawRoute(String resp) {
        LatLng loc, nextLoc;
        
        try {
            final JSONObject json = new JSONObject(resp);
            JSONArray routeArray = json.getJSONArray("routes");
            JSONObject routes = routeArray.getJSONObject(0);
            JSONObject overviewPolylines = routes.getJSONObject("overview_polyline");
            String encodeStr = overviewPolylines.getString("points");
            List<LatLng> list = decodePolyline(encodeStr);
            
            for (int i = 0; i < list.size() - 1; i++) {
                loc = list.get(i);
                nextLoc = list.get(i + 1);
                mMap.addPolyline(new PolylineOptions()
                        .add(new LatLng(loc.latitude, loc.longitude),
                                new LatLng(nextLoc.latitude, nextLoc.longitude))
                        .width(2)
                        .color(Color.BLUE));
            }
        } catch (JSONException e) {
        }
    }
    
    /* Called in drawRoute()
     * Reference: 
     * http://jeffreysambells.com/2010/05/27/decoding-polylines-from-google-maps-direction-api-with-java
     */
    private List<LatLng> decodePolyline(String encodeStr) {
        List<LatLng> locs = new ArrayList<LatLng>();
        int index = 0, len = encodeStr.length();
        int lat = 0, lng = 0;
        int b, shift, result;
        LatLng point;
        
        while (index < len) {
            shift = 0;
            result = 0;
            do {
                b = encodeStr.charAt(index++) - 63;
                result |= (b & 0x1f) << shift;
                shift += 5;
            } while (b >= 0x20);
            lat += ((result & 1) != 0 ? ~(result >> 1) : (result >> 1));
            
            shift = 0;
            result = 0;
            do {
                b = encodeStr.charAt(index++) - 63;
                result |= (b & 0x1f) << shift;
                shift += 5;
            } while (b >= 0x20);
            lng += ((result & 1) != 0 ? ~(result >> 1) : (result >> 1));
            
            point = new LatLng(((double)lat / 1E5), ((double)lng / 1E5));
            locs.add(point);
        }
        
        return locs;
    }
    
    private String getResponse(String strURL) throws IOException {
        HttpURLConnection urlConnection = null;
        InputStream in = null;
        String resp = "";
        
        try {
            URL url = new URL(strURL);
            urlConnection = (HttpURLConnection) url.openConnection();
            urlConnection.connect();
            in = urlConnection.getInputStream();
            BufferedReader br = new BufferedReader(new InputStreamReader(in));
            StringBuffer sb = new StringBuffer();
            
            String line = "";
            while ((line = br.readLine()) != null) {
                sb.append(line + "\n");
            }
            resp = sb.toString();
            br.close();
        } catch (Exception e) {
            Log.d("Error converting result", e.toString());
        } finally {
            in.close();
            urlConnection.disconnect();
        }
        
        return resp;
    }
    
    private class DrawTask extends AsyncTask<String, Void, String> {
        @Override
        protected String doInBackground(String... url) {
            String resp = "";
            
            try {
                resp = getResponse(url[0]); 
            } catch (Exception e) {
                Log.d("Background Task", e.toString());
            }
            
            return resp;
        }
        
        @Override
        protected void onPostExecute(String resp) {
            super.onPostExecute(resp);
            if (resp != null) {
                drawRoute(resp);
            }
        }
    }
}
