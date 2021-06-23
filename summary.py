# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 13:54:17 2021

@author: Satish Narasimhan

"""

import geocoder
from datetime import datetime
import static as s
import functions as f
import pandas as pd

# Provide list of mail id / recipients for each location
mailing_list = {
    "<<>>": 'Bengaluru'
    ,"<<>>" : 'Singapore' 
    ,"<<>>" : 'Bengaluru'
    ,"<<>>" : 'London'
    ,"<<>>" : 'Chennai'
     }

# Objects that are to be tracked
# Norad Id ISS - 25544, Hubble ST - 20580, Tianhe - 48274, X-37B - 45606
catalog = {
    "SPACE STATION - ISS": 25544
    ,"Hubble Space Telescope" : 20580
    ,"CSS - Tianhe" : 48274
    ,"USA 299 (Boeing X-37B, OTV 6)" : 45606
     }

# Obtain unique locations from the mailing list - set will produce unique. Convert the set to list
locations = list(set(mailing_list.values()))
print("Running script for the following locations:")
print(locations)

ids = list(set(catalog.values()))
print("Running script for the following catalog ids:")
print(ids)
print("------------------------------")

# Locations for which script is to be run
for loc in locations:
    g = geocoder.opencage( loc , key = s.open_cage_api_key)
    # Obtain Latitude and Longitude of location in search string
    coord = g.latlng
    
    city = g.city
    
    print(city,coord)
    lat = str(round(g.latlng[0],4))
    lon = str(round(g.latlng[1],4))
    
    dfObj = pd.DataFrame(columns=['Date','Time','View','Duration','Max. Elev.', 'Start Az', 'Max. Az', 'End Az', 'Mag.'])
    
    # For each location, check for flyby for each Norad_id
    for nid in ids:
        #norad_id = str(25544)
        print("Checking for: ",+(nid))
        norad_id = str(nid)
         
        const_url = [s.base_url,s.req_type, norad_id, lat, lon, s. alt, s.days, s.dur, s.append_api_key]
        
        visual_pass_url = f.url_const_ops('/',const_url)
        
        visual_pass_response = f.get_Response(visual_pass_url)
        #print(type(visual_pass_response))
        pairs = [   (key, value) 
            for key, values in visual_pass_response.items() 
            for value in values ]
        
        #print(type(pairs))
        
        for pair in pairs:
            #print(type(pair))
            print(pair)
            for key, values in pair.items():
                print('Key :: ', key)
                if(isinstance(values, list)):
                    for value in values:
                        print(value)
                else:
                    print(value)    
            
        
        
        risetime = f.extract_element_from_json(visual_pass_response, ["passes","startUTC"])
        maxEl = f.extract_element_from_json(visual_pass_response, ["passes","maxEl"])
            
        duration = f.extract_element_from_json(visual_pass_response, ["passes","duration"])
        start_az = f.extract_element_from_json(visual_pass_response, ["passes","startAz"])
        max_az = f.extract_element_from_json(visual_pass_response, ["passes","maxAz"])
        end_az = f.extract_element_from_json(visual_pass_response, ["passes","endAz"])
        start_dir = f.extract_element_from_json(visual_pass_response, ["passes","startAzCompass"])
        max_dir = f.extract_element_from_json(visual_pass_response, ["passes","maxAzCompass"])
        end_dir = f.extract_element_from_json(visual_pass_response, ["passes","endAzCompass"])
        magnitude = f.extract_element_from_json(visual_pass_response, ["passes","mag"])
        
        satname = f.extract_element_from_json(visual_pass_response, ["info","satname"])
        print(type(risetime), type(satname), type(duration))
        print(risetime)
        print(satname)
        print(duration[1])
        # Capturing all relevant recipients for the location
        recipients = f.getKeysByValue(mailing_list, loc)
        print(loc, recipients)
        print(maxEl[0])
        
        for i in range (0, len(risetime)):
            flybydate = datetime.fromtimestamp(risetime[i]).strftime("%A, %d %B %Y")
            flybytime = datetime.fromtimestamp(risetime[i]).strftime("%I:%M %p")
                  
            if (str(magnitude[i]) == 'None'):
                magnitude[i] = 3
       
            if (magnitude[i] <= (-1.8)):
                visibility = "Excellent"
            elif(magnitude[i] > (-1.8) and magnitude[i] <= (-0.8) ):
                visibility = "Good"
            elif(magnitude[i] > (-0.8) and magnitude[i] <= (0.8) ):
                visibility = "Marginal"
            else:
                visibility = "Poor"
            view = 'Visibility : ' + visibility
            mag = 'Magnitude:'+ str(magnitude[i])
            duration = duration[i]
            max_height = 'Max. Height: '+ str(maxEl[i]) + '°'
            start_az_dir = (str(round(start_az[i]%180,0))+'-'+start_dir[i]) , 
            max_az_dir = (str(round(max_az[i]%180,0))+'-'+max_dir[i]), 
            end_az_dir = (str(round(end_az[i]%180,0))+'-'+end_dir[i]),
                        
            dfObj = dfObj.append({'Date':risetime,'Time': risetime,'View': visibility,'Duration': duration,'Max. Elev.': maxEl[i],'Start Az': start_az_dir , 'Max. Az' : max_az_dir,'End Az' : end_az_dir,'Mag.': magnitude[i]}, ignore_index = True)
                
            uname ='"<<>>"'
            to = uname    
            header = satname[0]
            subject = 'Sky Watcher Alert - ' + header
            contents = [header, "\n", loc, "\n", dfObj]
            #contents = [header, loc, flybydate, flybytime, view, duration, max_height, details, mag]
            #print(dfObj)
            
            
            #print(to, '\n', subject, '\n',contents, '\n', recipients)
    
if (dfObj.empty == False):
    print(dfObj)
    #yagmail.SMTP(uname).send(to, subject, contents, bcc = recipients)
    print('Email sent successfully . . .')
    print("=======================================")
else:
    print("No visibile passes")
    print("=======================================")