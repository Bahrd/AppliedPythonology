from matplotlib.pyplot import show, title, bar, yticks, figure, plot
from matplotlib.colors import LinearSegmentedColormap as lscm
from numpy import histogram, arange, min, max

'''
import matplotlib.pyplot as plt
import numpy as np

# Plot 1
x = np.array([0.0, 0.1, 0.2, 0.3])
y = np.array([3, 8, 1, 10])
plt.bar(x*10, y, color = 'r', alpha = 0.7)

# Plot 2
x = np.array([-0.3, -0.2, -0.1, 0.0, 0.1])
y = np.array([10, 20, 30, 40, 50])
plt.bar(x*10, y, color = 'b', alpha = 0.7)

# Plot 2
x = np.array([0.5, 0.6, 0.7])
y = np.array([-1, 1, 2])
plt.bar(x*10, y, color = 'g', alpha = 0.7)

plt.show()
exit()
'''
def channelGradientHistogram(img, art, name, channels, N = 0x100, DC = False, tabs = None):
    # Good ol transposition trick
    hC, hX = zip(*[histogram(img[..., c], bins = N) for c in range(len(channels))])

    if(tabs != None): _ = figure()
    for h, x, cr in zip(hC, hX, channels):
        ## Color map build-up (Have you already sensed a smell of interpolation here? ;)
        cm = lscm.from_list(cr[0], cr[1:], N = N)
        colors = cm(arange(N))
        # Sometimes the 🗲DC🗲 is the zeroth component that is overwhelmingly large
        # (yet still hardly interesting)!
        if(DC == False): h[0] = 0
        nx = x[1:]*0xff/(max(x[1:]) - min(x[1:])) # Bar-normalized x-axis
        bar(nx, h, color = colors, alpha = .75, width = 1)
    title(f'{art} in {name} space'); yticks([])
    if(tabs != None): 
        tabs.addPlot(f'{art} in {name} space', _)
    else:
        show()

if __name__ == '__main__':
    from histogramXYZ import channelGradientHistogram as cgh # ;)
    from auxiliary import (RGB_ext_channels as RGB, YCbCr_ext_channels as YCbCr, YCoCg_ext_channels as YCoCg,
                           YCbCr2RGB, YCoCg2RGB)
    from imports.plotWindow import plotWindow as mtw
    import matplotlib.pyplot as plt
    from sys import argv

    
    tabs = mtw()
    art = './images/Pollock No. 5.png' if len(argv) < 0b10 else argv[1]
    img = plt.imread(f'{art}')[..., :3]

    kwargs = ({'img': img, 'art': art, 'name': 'RGB in cgh', 'channels': RGB},
              {'img': img@YCbCr2RGB.T, 'art': art, 'name': 'YCbCr in cgh', 'channels': YCbCr},
              {'img': img@YCoCg2RGB.T, 'art': art, 'name': 'YCoCg in cgh', 'channels': YCoCg})
    for kwarg in kwargs:
        cgh(**kwarg, tabs = tabs)
    tabs.show()