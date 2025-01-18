﻿import cv2 as openCV

from sys import argv
from numpy import histogram, arange
from matplotlib.pyplot import show, title, bar, yticks
from matplotlib.colors import LinearSegmentedColormap as lscm

def channelGradientHistogram(img, art, name, channels, N = 0x100):
    redux = lambda x: x[0]
    hC = [redux(histogram(img[..., c], bins = N)) for c in range(0b11)]

    for h, cr in zip(hC, channels):
        cm = lscm.from_list(cr[0], cr[1:], N = N)
        colors = cm(arange(N))
        bar(range(len(h)), h, color = colors, width = 1, alpha = .75)
    title(f'{art} in {name}'); yticks([])
    show()

if __name__ == '__main__':
    from histogramXYZ import channelGradientHistogram as CHXYZ # ;)
    from auxiliary import RGB_channels as RGB
    art = './images/Pollock No. 5.png' if len(argv) < 0b10 else argv[1]
    img = openCV.cvtColor(openCV.imread(f'{art}'), openCV.COLOR_BGR2RGB)
    CHXYZ(img, art, 'RGB', RGB)