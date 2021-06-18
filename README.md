# Skywatch
Skywatch is for space station spotters. 

This program / module will provide details of the next pass of a space object as identified by it's Norad id.
The script currently caters to :
1. International Space Station (ISS)
2. Hubble Space Telescope (HST)
3. Tianhe - Chinese Space Station (CSS)
4. Boeing X-37B

The script is built to provide you the following details:
1. Date and time of the pass
2. Direction of the pass
3. Magnitude of the pass i.e. relative visibility
4. Duration of the pass

An email alert has been incorporated with the script. 

Email id's and locations of the intended audience is to be provided by the user.

This project has been built primarily from an academic / space station spotting hobby view point.

API's required are:
1. Geocoder - Open Cage API
2. One of Celestrak or N2YO API

SMTP Email id is to be configured using yagmail - https://pypi.org/project/yagmail/
