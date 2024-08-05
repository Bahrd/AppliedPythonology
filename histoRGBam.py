import cv2

from sys import argv
from numpy import histogram, arange, linspace, concatenate
from matplotlib.pyplot import plot, show, xticks, yticks, title

art = './images/Pollock No. 5.png' if len(argv) < 0b10 else argv[1]
img = cv2.cvtColor(cv2.imread(f'{art}'), cv2.COLOR_BGR2RGB)

redux = lambda x: x[0]
hR, hG, hB = [redux(histogram(img[..., c], bins = 0x100)) for c in range(0b11)]
maxRGB = max(concatenate([hR, hG, hB]))

xticks(arange(0, 0x101, 0x20)); yticks(linspace(0, maxRGB, 0o12))
plot(hR, 'r', hG, 'g', hB, 'b'); title(art); show()
