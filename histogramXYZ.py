from matplotlib.pyplot import show, title, bar, yticks, figure
from matplotlib.colors import LinearSegmentedColormap as lscm
from numpy import histogram, arange

from auxiliary import YCoCg2RGB

def channelGradientHistogram(img, art, name, channels, N = 0x100, DC = True, tabbed = None):
    redux = lambda x: x[0]
    hC = [redux(histogram(img[..., c], bins = N)) for c in range(len(channels))]

    if(tabbed != None): _ = figure()
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
    if(tabbed != None): 
        tabbed.addPlot(f'{art} in {name} space', _)
    else:
        show()

if __name__ == '__main__':
    from cv2 import cvtColor as cvcc, imread as cvread, COLOR_BGR2RGB
    from histogramXYZ import channelGradientHistogram as cgh # ;)
    from auxiliary import RGB_ext_channels as RGB, YCbCr_ext_channels as YCbCr, YCoCg_ext_channels as YCoCg
    from auxiliary import YCbCr2RGB, YCoCg2RGB
    from sys import argv
    from imports.plotWindow import plotWindow as pw
    from matplotlib.pyplot import figure as fg

    
    tabs = pw()
    art = './images/Pollock No. 5.png' if len(argv) < 0b10 else argv[1]
    img = cvcc(cvread(f'{art}'), COLOR_BGR2RGB); 

    _ = fg()
    cgh(img, art, 'RGB in cgh', RGB, noshow = True)
    tabs.addPlot('RGB', _)

    _ = fg()
    cgh(img@YCbCr2RGB, art, 'YCbCr in cgh', YCbCr, noshow = True)
    tabs.addPlot('YCbCr', _)

    _ = fg()
    cgh(img@YCoCg2RGB, art, 'YCoCg in cgh', YCoCg, noshow = True)
    tabs.addPlot('YCoCg', _)

    tabs.show()