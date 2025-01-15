## A frame collection to MP4 transcoder
# See the source: https://medium.com/@iKhushPatel/convert-video-to-images-images-to-video-using-opencv-python-db27a128a481

from cv2 import imread, VideoWriter, VideoWriter_fourcc
from os.path import isfile, join
from os import listdir
from sys import argv
from re import compile

## Collect image filenames from a given directory with extension[s]
#  that match[es] the pattern and pack'em all into a single 'avi' file...
#  ./img2mpg.py './', 'jpe?g' './avis/⅄⅂LY.avi'
pathIn, ext, pathOut = argv[1:4]
pattern = compile(ext)
files = [f for f in listdir(pathIn)
           if isfile(join(pathIn, f)) and pattern.search(f.lower())]

#Sort the filenames (ignoring extension [assumed to exist] because... why not?)
# https://stackoverflow.com/questions/12453580/how-to-concatenate-join-items-in-a-list-to-a-single-string
files.sort(key = lambda x: '.'.join(x.split('.')[: -1]))

## Setting the video encoder parameters
fps, fourcc = 50, VideoWriter_fourcc(*'DIVX')
# Take a video size from the first frame
frame = imread(join(pathIn, files[0]))
size = frame.shape[: 2]                                  # Ignore the 'layers' parameter
out = VideoWriter(pathOut, fourcc, fps, size[:: -1]) # Swap rows/cols

## Compose images into a movie...
for f in files:
    frame = imread(join(pathIn, f))
    print(f)
    # Assemble frames into a video stream
    out.write(frame)

out.release()