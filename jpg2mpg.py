## A JP(E)G to MP4 transcoder 
# 'C:\Users\Przem\source\repos\Bahrd\images\jpgs'
#
# See the source: https://medium.com/@iKhushPatel/convert-video-to-images-images-to-video-using-opencv-python-db27a128a481

import cv2
from os.path import isfile, join
from re import search, compile

## Collect JP(E)G filenames
pathIn, pathOut, ext = '../images/jpgs/', '../images/jpgs/video.mp4', 'jpe?g'
pattern = re.compile(ext)
files = [f for f in os.listdir(pathIn) 
           if isfile(join(pathIn, f)) and pattern.search(f.lower())]

#Sort the filenames (ignoring extension)
files.sort(key = lambda x: x[0: -len(ext)])

## Compose images into an array
frame_array = [cv2.imread(join(pathIn, f)) for f in files]

## Setting the video encoder parameters
fps, fourcc = 4, cv2.VideoWriter_fourcc(*'DIVX')
# Take a video size from the first frame 
size = frame_array[0].shape[: 2]          # Ignore the 'layers' parameter             
out = cv2.VideoWriter(pathOut, fourcc, fps, size[:: -1]) # Swap rows/cols
# Assemble frames in a video stream
for f in frame_array:
    out.write(f)
out.release()
