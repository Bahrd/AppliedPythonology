## EXIF GPS tags transplantation ('allografts')
#  Copies the GPS tags from a file 'names[1]' to all 'names[2:]'
import piexif as pxf
from sys import argv as names

# Donor and recipient names (command line arguments)
_ = len(names)
if(_ > 1):
    donor, recipients = names[1], names[2:]
    # GPS tags procurement, transport...
    exif = pxf.load(donor)
    gps = exif['GPS']

    if(_ > 2):
        # ... and the transplantation(s)
        for recipient in recipients:
            exif = pxf.load(recipient)
            exif['GPS'] = gps
            pxf.insert(pxf.dump(exif), recipient)
            print(recipient)
    else:
        cardinal_directions = (gps[1].decode('utf-8'), gps[3].decode('utf-8'))
        #                         36°            50'                      28.42''                      N
        latitude =  f"{gps[2][0][0]}°{gps[2][1][0]}'{gps[2][2][0]/gps[2][2][1]}''{cardinal_directions[0]}"
        #                        117°             5'                      26.24''                      W
        longitude = f"{gps[4][0][0]}°{gps[4][1][0]}'{gps[4][2][0]/gps[4][2][1]}''{cardinal_directions[1]}"
        print(f'{donor} was taken at:')
        print(latitude)
        print(longitude)
else:
    print('USAGE: exifGPStransplant donor recipient1 [recipient2 ...]')

