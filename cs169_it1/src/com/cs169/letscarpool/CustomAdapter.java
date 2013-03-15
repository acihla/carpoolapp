package com.cs169.letscarpool;
import java.util.ArrayList;

import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

public class CustomAdapter extends BaseAdapter {
 
    private ArrayList<SearchResultDetails> resultsAr;
    Context context;
    
    CustomAdapter (ArrayList<SearchResultDetails> data, Context c){
        resultsAr = data;
        context = c;
    }
   
    public int getCount() {
        // TODO Auto-generated method stub
        return resultsAr.size();
    }
    
    public Object getItem(int position) {
        // TODO Auto-generated method stub
        return resultsAr.get(position);
    }
 
    public long getItemId(int position) {
        // TODO Auto-generated method stub
        return position;
    }
   
    public View getView(int position, View convertView, ViewGroup parent) {
        // TODO Auto-generated method stub
         View v = convertView;
         if (v == null)
         {
            LayoutInflater vi = (LayoutInflater)context.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
            v = vi.inflate(R.layout.list_search_result, null);
         }
 
           ImageView image = (ImageView) v.findViewById(R.id.icon);
           TextView usernameView = (TextView)v.findViewById(R.id.username_result);
           TextView mapInfoView = (TextView)v.findViewById(R.id.map_info_result);
           TextView departTimeView = (TextView)v.findViewById(R.id.time_depart_result);
           TextView avegRatingView = (TextView)v.findViewById(R.id.aveg_rating_result);
           Button detailsButton = (Button)v.findViewById(R.id.details_button);
           SearchResultDetails msg = resultsAr.get(position);
           image.setImageResource(msg.icon);
           usernameView.setText(msg.username);
           String departdatetime = msg.depart_time;
//           departTimeView.setText("Depart Date: " + departdatetime.substring(0,departdatetime.indexOf("T"))
//        		   				+ " Time: " +departdatetime.substring(departdatetime.indexOf("T")+1, departdatetime.indexOf(".")));
           departTimeView.setText(departdatetime);
           mapInfoView.setText("Map Info: " + msg.map_info);
           avegRatingView.setText("Average Rating: "+msg.aveg_rating);                             
           
          
//           detailsButton.setOnClickListener(new View.OnClickListener() {              
//                   public void onClick(View v) {
//                   // TODO Auto-generated method stub
//                   AlertDialog.Builder adb=new AlertDialog.Builder(this);
//                   adb.setMessage("Add To Contacts?");
//                   adb.setNegativeButton("Cancel", null);
//                   final int selectedid = position;
//                   final String itemname= (String) resultsAr.get(position).getName();
// 
//                   adb.setPositiveButton("OK", new AlertDialog.OnClickListener() {
//                       public void onClick(DialogInterface dialog, int which) {
//                                  
//                              //Your working   
//                           }});
//                  
//                   adb.show();  
//               } 
//           });
//                        
        return v;
}
    
}