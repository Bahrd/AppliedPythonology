## EXIF GPS tags transplantation ('allografts')
#  Copies the GPS tags from a file 'names[1]' to all 'names[2:]'
import piexif as pxf
from sys import argv as names

# Donor and recipient names (command line arguments)
donor, recipients = names[1], names[2:]

# GPS tags procurement, transport...
exif = pxf.load(donor)
GPS = exif['GPS']

# ... and the transplantation(s)
for recipient in recipients:
    exif = pxf.load(recipient)
    exif['GPS'] = GPS
    pxf.insert(pxf.dump(exif), recipient)

## EXIF GPS tags hand-crafted modification ('autografts')...
'''
from exif import Image
import sys

with open('Yosemite Valley.JPEG', 'rb') as in_image_file:
    img = Image(in_image_file)
# Note the GPS tags format
# Yosemite Valley: 37° 43′ 18″ N, 119° 38′ 47″ W
img.gps_latitude = (37.0, 43.0, 18.0)
img.gps_longitude = (119.0, 38.0, 47.0)
img.gps_altitude = 1200
with open('Yosemite Valley.JPEG', 'wb') as out_image_file:
    out_image_file.write(img.get_file())

## Other locations...
# Mocassin (Tuolumne Count, CA): 37° 48′ 39″ N, 120° 18′ 0″ W
# Hollywood Sign Puzzle View: 34°06'18.3"N 118°19'52.0"W
# Hoover Dam: 36° 0′ 56″ N, 114° 44′ 16″ W
# Rainbow Canyon: 36° 21′ 56.88″ N, 117° 30′ 5.4″ W
# Route 66 (AZ): 35°14'15.5"N 113°12'22.6"W


'''