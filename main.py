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
import yagmail

# Provide list of mail id / recipients for each location
mailing_list = {
     "email1@gmail.com": 'Bengaluru'
    ,"email2@gmail.com" : 'Singapore' 
    ,"email3@gmail.com" : 'Chennai'
    ,"email4@gmail.com" : 'Bengaluru' 
    ,"email5@icloud.com" : 'London'
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
    g = geocoder.opencage( loc , key ='3dd3a312e17a45268ba666353daa25bf')
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
        
        # Filters out passes below this maximum elevation threshold
        max_el_filter = 40 
        # Filters out passes above this magnitude threshold. 
        # values are ISS = (-0.9); HST = 4.9;Tianhe-1 = 100001; X37B =100001
        mag_filter = (100001) 
        satname = f.extract_element_from_json(visual_pass_response, ["info","satname"])
        
        # Capturing all relevant recipients for the location
        recipients = f.getKeysByValue(mailing_list, loc)
        print(loc, recipients)
        print(maxEl[0])
        send_email = 'Y'
        
        if (str(magnitude[0]) == 'None'):
            magnitude[0] = 3
            
        print(magnitude[0])
        
        if (magnitude[0] <= (-1.8)):
            visibility = "Excellent"
        elif(magnitude[0] > (-1.8) and magnitude[0] <= (-0.8) ):
            visibility = "Good"
        elif(magnitude[0] > (-0.8) and magnitude[0] <= (0.8) ):
            visibility = "Marginal"
        else:
            visibility = "Poor"
        
         
        if (visibility == "Poor"):
            send_email = 'N'
        
        print(visibility, send_email)
        
        if (send_email == 'Y'):
        # Email is being sent only for the first / earliest record
            flybydate = datetime.fromtimestamp(risetime[0]).strftime("%A, %d %B %Y")
            flybytime = datetime.fromtimestamp(risetime[0]).strftime("%I:%M %p")
                    
            if (maxEl[0] >= (max_el_filter)): 
                if(magnitude[0] < (mag_filter)):
                    view = 'Visibility : ' + visibility
                    mag = 'Magnitude:'+ str(magnitude[0])
                    duration = str(round(duration[0]/60,0))+' mins'
                    max_height = 'Max. Height: '+ str(maxEl[0]) + '°'
                    start_az_dir = (str(round(start_az[0]%180,0))+'-'+start_dir[0]) , 
                    max_az_dir = (str(round(max_az[0]%180,0))+'-'+max_dir[0]), 
                    end_az_dir = (str(round(end_az[0]%180,0))+'-'+end_dir[0]),
                    
                    dfObj = dfObj.append({'Date':flybydate,'Time': flybytime,'View': visibility,'Duration': duration,'Max. Elev.': maxEl[0],'Start Az': start_az_dir , 'Max. Az' : max_az_dir,'End Az' : end_az_dir,'Mag.': magnitude[0]}, ignore_index = True)
                    
                    uname = s.to
                    to = uname    
                    header = satname[0]
                    subject = 'Sky Watcher Alert - ' + header
                    contents = [header, "\n", loc, "\n", dfObj]
                    #contents = [header, loc, flybydate, flybytime, view, duration, max_height, details, mag]
                    #print(dfObj)
                    
                    
                    #print(to, '\n', subject, '\n',contents, '\n', recipients)
    
    if (dfObj.empty == False):
        print(dfObj)
        yagmail.SMTP(uname).send(to, subject, contents, bcc = recipients)
        print('Email sent successfully . . .')
        print("=======================================")
    else:
        print("No visibile passes")
        print("=======================================")