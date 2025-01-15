import cv2 as openCV

from sys import argv
from numpy import histogram, arange, linspace, concatenate
from matplotlib.pyplot import plot, show, xticks, yticks, title

art = './images/Pollock No. 5.png' if len(argv) < 0b10 else argv[1]
img = openCV.cvtColor(openCV.imread(f'{art}'), openCV.COLOR_BGR2RGB)

redux = lambda x: x[0]
hR, hG, hB = [redux(histogram(img[..., c], bins = 0x100, density = True)) for c in range(0b11)]
maxRGB = max(concatenate([hR, hG, hB]))

xticks(arange(0, 0x101, 0x20)); yticks([])
plot(hR, 'r', hG, 'g', hB, 'b'); title(art); show()
