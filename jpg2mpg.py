## A JP(E)G to MP4 transcoder 
# 'C:\Users\Przem\source\repos\Bahrd\images\jpgs'
#
# See the source: https://medium.com/@iKhushPatel/convert-video-to-images-images-to-video-using-opencv-python-db27a128a481

import cv2
from os.path import isfile, join
from os import listdir
from re import search, compile

## Collect JP(E)G filenames
pathIn, pathOut, ext = '../images/jpgs/', '../images/jpgs/video.mp4', 'jpe?g'
pattern = compile(ext)
files = [f for f in listdir(pathIn) 
           if isfile(join(pathIn, f)) and pattern.search(f.lower())]

#Sort the filenames (ignoring extension)
files.sort(key = lambda x: x[0: -len(ext)])

## Setting the video encoder parameters
fps, fourcc = 25, cv2.VideoWriter_fourcc(*'DIVX')
# Take a video size from the first frame 
frame = cv2.imread(join(pathIn, files[0]))
size = frame.shape[: 2]          # Ignore the 'layers' parameter             
out = cv2.VideoWriter(pathOut, fourcc, fps, size[:: -1]) # Swap rows/cols

print(size[:: -1])

## Compose images into an array
for f in files:
    frame = cv2.imread(join(pathIn, f))
    print(f)
    # Assemble frames in a video stream
    out.write(frame)

out.release()