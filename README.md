# Applied Pythonology
![Laocoön and His Sons](https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/Laocoon_Pio-Clementino_Inv1059-1064-1067.jpg/250px-Laocoon_Pio-Clementino_Inv1059-1064-1067.jpg)
## Basic system identification and image & graphics processing (a.k.a. '*machine learning*' and '*machine vision**') algorithms
### Low-level image and data processing
- interpolation
  - 1D: [interpolation1D.ipynb](./interpolation1D.ipynb) & [interpolation1D.py](./interpolation1D.py)
  - 2D: [interpolation2D.py](./interpolation2D.py)
- simple scaling and rotation: [rotatioNN.py](./rotatioNN.py) and [rotation2D.py](./rotation2D.py)
- demosaicking (for **Bayer's** and X-Trans® CFAs): [demosaicking.py](./demosaicking.py) and [demosaickingX.py](./demosaickingX.py)
- **Cooley-Tukey's** FFT: [CooleyTukey.py](./CooleyTukey.py)
- low-light image generation: [PoissonedJupiter.py](./PoissonedJupiter.py) and [PoissoningMBA](./PoissoningMBA)
- Monte Carlo pixel counting/area measurements: [MonteCarlo.py](./MonteCarlo.py)
- denoising by DCT or wavelet thresholding: [DCT.py](./dct.py) and [WaveletThresholding.py](./WaveletThresholding.py)
- **Duda's** ANS compression coding: [ans.py](./ans.py)
- JPEG 'lite' algorithm: [jpglite.py](./jpglite.py)
- JPEG 2000 'featherlite' algorithm: [J2K.py](./J2K.py)
- **Hamming's** code: [HammingBird.ipynb](./HammingBird.ipynb) and [HammingBird.py](./HammingBird.py)
- cryptography: PKI [RSA.py](./RSA.py), key-exchange [DHM.py](./DHM.py) and zero knowledge proof [ZKP.py](./ZKP.py) ([ECC.pl](./ECC.pl) *in statu nascendi*)
- **Julia's** and **Mandelbrot's** fractals visualisations: [julia.py](./julia.py) and [mandelbrot.py](./mandelbrot.py)
### Modeling and identification
- pseudo-random number generator: [pseudogenerator.py](./pseudogenerator.py)
- **Tukey's** potion: [TukeyPotion.py](./TukeyPotion.py)
- function regression estimation with _L<sub>2</sub>_ cost function and _L<sub>q</sub>_ constraints: [regressionCVX.py](./regressionCVX.py)
- **Julia's** and **Mandelbrot's** fractals (yes, again, but now as a nonlinear dynamic phenomena): [julia.py](./julia.py) and [mandelbrot.py](./mandelbrot.py)
- **Collatz's** conjecture visualization: [collatz.py](./collatz.py)
- Golden Section Search: [GSS.py](./GSS.py)
- **Bayes'** theorem: [Bayes4all.ipynb](./Bayes4all.ipynb) and [Bayes4all.py](./Bayes4all.py)
- **Monty Hall's** (no-)problem: [MontyHall.py](./montyhall.py)
### Computer graphics
- Polar squares and scary circles: [PolarAndPolygon.py](./PolarAndPolygon.py)
- **Bézier** curves: [deBézier.py](./deBézier.py) and [rationalBézier.py](./rationalBézier.py)
- **Bresenham's** line [bresenhamLine.py](./bresenhamLine.py) and circle: [bresenhamCircle.py](./bresenhamCircle.py)
- CGAL in action: [wedge.scad](./CGAL4All/wedge.scad)