## EXIF GPS tags transplantation ('allografts')
#  Copies the GPS tags from a file 'names[1]' to all 'names[2:]'
import piexif as pxf
from sys import argv as names

# Donor and recipient names (command line arguments)
if(len(names) < 3):
    print('USAGE: exifGPStransplant donor recipient1 [recipient2 ...]')
    exit(-1)
else:
    donor, recipients = names[1], names[2:]

# GPS tags procurement, transport...
exif = pxf.load(donor)
gps = exif['GPS']

# ... and the transplantation(s)
for recipient in recipients:
    exif = pxf.load(recipient)
    exif['GPS'] = gps
    pxf.insert(pxf.dump(exif), recipient)
    print(recipient)