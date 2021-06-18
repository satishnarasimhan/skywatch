# -*- coding: utf-8 -*-
"""
Created on Mon May 24 13:01:59 2021

@author: Satish Narasimhan
"""
# API Keys
open_cage_api_key = '<<Open Cage APi Key>>'
api_key = '<<Celetrak or N2YO API key>>' 

# Request URL parameters
req_type = 'visualpasses' # tle, visualpasses, positions, radiopasses - default visualpasses
base_url = '<<Base URL>>'
append_api_key = ('&apiKey=')+api_key

# Altitude in meters
alt = str(0)
# Duration for which pass is visible in seconds 
dur = str(30)
# number of days. Max is 10 
days = str(10) 

# Mailing List - From / Sender
to = 'sender email id'
