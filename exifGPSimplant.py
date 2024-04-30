## EXIF GPS tags hand-crafted modification ('autografts')...
from exif import Image
from sys import argv as names
from math import floor

def dd_GPS_dms(coordinate):
    latlonitude = float(coordinate)
    degrees = floor(latlonitude)
    residuum = (latlonitude - degrees) * 60
    minutes = floor(residuum)
    seconds = (residuum - minutes) * 60

    return (degrees, minutes, seconds)

if(len(names) < 4):
    print('USAGE: exifGPSimplant filename latitude [0-360) longitude [0 - 180)')
    exit(-1)
else:
    (recipient, latitude, longitude) = names[1:4]

with open(recipient, 'rb') as image_file:
    img = Image(image_file)

img.gps_latitude = dd_GPS_dms(latitude)
img.gps_longitude = dd_GPS_dms(longitude)
#img.gps_altitude = 1200 # An orphan...

print(img.gps_latitude, img.gps_longitude)

with open(recipient, 'wb') as image_file:
    image_file.write(img.get_file())

'''
Note the GPS tags format
34°56'43.386"N 109°46'32.447"W
# Other locations...
https://www.gps-coordinates.net/gps-coordinates-converter
Whitewater, CA: 33.923685, -116.640324
Yosemite Valley: 37° 43′ 18″ N, 119° 38′ 47″ W
Mocassin (Tuolumne Count, CA): 37° 48′ 39″ N, 120° 18′ 0″ W
Hollywood Sign Puzzle View: 34°06'18.3"N 118°19'52.0"W
Hoover Dam: 36° 0′ 56″ N, 114° 44′ 16″ W
Rainbow Canyon: 36° 21′ 56.88″ N, 117° 30′ 5.4″ W
Route 66 (AZ): 35°14'15.5"N 113°12'22.6"W
Las Vegas' Replica of the Statue of Liberty 36°6'3.58"N 115°10'23.029"W
The Tepees in Petrified Forest 34°56'43.386"N 109°46'32.447"W
Golden gate & Alcatraz: 37.7764931, 122.5042172
Monument Valley: 36.985492 110.1947339,464

Tucson's 32.171897 110.989734
'''