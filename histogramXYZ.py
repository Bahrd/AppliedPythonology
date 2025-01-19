from matplotlib.pyplot import show, title, bar, yticks
from matplotlib.colors import LinearSegmentedColormap as lscm
from numpy import histogram, arange

def channelGradientHistogram(img, art, name, channels, N = 0x100, DC = True):
    redux = lambda x: x[0]
    hC = [redux(histogram(img[..., c], bins = N)) for c in range(len(channels))]

    for h, cr in zip(hC, channels):
        ## Color map build-up
        cm = lscm.from_list(cr[0], cr[1:], N = N)
        colors = cm(arange(N))
        # Sometimes the 🗲DC🗲 (zeroth) component is overwhelmingly large
        # (yet still hardly interesting)!
        if(DC == False): h[0] = 0
        bar(range(len(h)), h, color = colors, width = 1, alpha = .75)
    title(f'{art} in {name} space'); yticks([])
    show()

if __name__ == '__main__':
    from cv2 import cvtColor as cvcc, imread as cvread, COLOR_BGR2RGB
    from histogramXYZ import channelGradientHistogram as CHXYZ # ;)
    from auxiliary import RGB_channels as RGB
    from sys import argv

    art = './images/Pollock No. 5.png' if len(argv) < 0b10 else argv[1]
    img = cvcc(cvread(f'{art}'), COLOR_BGR2RGB)
    CHXYZ(img, art, 'RGB', RGB)