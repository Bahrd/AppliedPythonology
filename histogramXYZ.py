from matplotlib.pyplot import show, title, bar, yticks, figure
from matplotlib.colors import LinearSegmentedColormap as lscm
from numpy import histogram, arange

def channelGradientHistogram(img, art, name, channels, N = 0x100, DC = True, tabs = None):
    redux = lambda x: x[0]
    hC = [redux(histogram(img[..., c], bins = N)) for c in range(len(channels))]

    if(tabs != None): _ = figure()
    for h, cr in zip(hC, channels):
        ## Color map build-up (Have you already sensed a smell
        #  of interpolation here? ;)
        cm = lscm.from_list(cr[0], cr[1:], N = N)
        colors = cm(arange(N))
        # Sometimes the 🗲DC🗲 (zeroth) component is overwhelmingly large
        # (yet still hardly interesting)!
        if(DC == False): h[0] = 0
        bar(range(len(h)), h, color = colors, width = 1, alpha = .75)
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