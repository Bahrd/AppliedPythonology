# Applied Pythonology
![Laocoön and His Sons](https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/Laocoon_Pio-Clementino_Inv1059-1064-1067.jpg/250px-Laocoon_Pio-Clementino_Inv1059-1064-1067.jpg)
## Basic image & graphics processing (a.k.a. '*machine learning*' and '*machine vision*') algorithms
### Low-level data (image and signal) processing
- interpolation
  - 1D: [interpolation1D.ipynb](./interpolation1D.ipynb) & [interpolation1D.py](./interpolation1D.py)
  - 2D: [interpolation2D.ipynb](./interpolation2D.ipynb) & [interpolation2D.py](./interpolation2D.py)
- simple 2D scaling and rotation
    - NN:  [rotatioNN.ipynb](./rotatioNN.ipynb) & [rotatioNN.py](./rotatioNN.py)
    - spline: [rotation2D.ipynb](./rotation2D.ipynb) & [rotation2D.py](./rotation2D.py)
- demosaicking CFAs
  - **Bayer's**: [demosaicking.py](./demosaicking.py)
  -  and X-Trans®: [demosaickingX.py](./demosaickingX.py)
- **Cooley-Tukey's** FFT: [CooleyTukey.py](./CooleyTukey.py)
- low-light image generation: [PoissonedJupiter.py](./PoissonedJupiter.py) and [PoissoningMBA](./PoissoningMBA)
- **Poisson** to **Gauss** (**Anscombe**) transform: [Anscombe.ipynb](./Anscombe.ipynb) and [Anscombe.py](./Anscombe.py) 
- denoising by DCT or wavelet thresholding: [DCT.py](./dct.py) and [WaveletThresholding.py](./WaveletThresholding.py)
- Monte Carlo pixel counting/area measurements: [MonteCarlo.py](./MonteCarlo.py)
- **Duda's** ANS compression coding:  [ans.ipynb](./ans.ipynb) & [ans.py](./ans.py)
- JPEG 'lite' algorithm: [jpglite.py](./jpglite.py)
- JPEG 2000 'featherlite' algorithm: [J2K.py](./J2K.py)
- **Hamming's** code: [HammingBird.ipynb](./HammingBird.ipynb) and [HammingBird.py](./HammingBird.py)
- jigsaw pieces of cryptography: 
  - PKI [RSA.py](./RSA.py), 
  - key-exchange [DHM.py](./DHM.py), 
  - zero knowledge proof [ZKP.py](./ZKP.py) and 
  - elliptic curves [ECC.pl](./ECC.pl)
### Modeling and identification
- pseudo-random number generator: [pseudogenerator.py](./pseudogenerator.py)
- **Tukey's** potion (sans **Cooley**): [TukeyPotion.py](./TukeyPotion.py)
- function regression estimation with _L<sub>2</sub>_ cost function and _L<sub>q</sub>_ constraints: [regressionCVX.py](./regressionCVX.py)
- **Collatz's** conjecture visualization: [collatz.py](./collatz.py)
- **Kiefer's** Golden Section Search: [GSS.py](./GSS.py)
- **Bayes'** theorem: [Bayes4all.ipynb](./Bayes4all.ipynb) and [Bayes4all.py](./Bayes4all.py)
- **Monty Hall's** (no-)problem: [MontyHall.py](./montyhall.py)
### Computer graphics
- **Gauss** Circle problem: [latticeCircle.ipynb](./latticeCircle.ipynb) and [latticeCircle.py](./latticeCircle.py)
- polar squares and scary circles: [PolarAndPolygon.py](./PolarAndPolygon.py)
- **Bresenham's** algorithms:
  - line [bresenhamLine.py](./bresenhamLine.py)
  - circle: [bresenhamCircle.py](./bresenhamCircle.py)
- **Bézier's** 
  - curves: [deBézier1D.py](./deBézier1D.py) and [deBézieRat1D.py](./deBézieRat1D.py) (rational)
  - surfaces: [deBézier2D.py](./deBézier2D.py) 
- matrix transformations in 2D: [MatrixTransforms2D.ipynb](./MatrixTransforms2D.ipynb) and [MatrixTransforms2D.py](./MatrixTransforms2D.py)
- a little [CGAL](https://www.cgal.org/) in action: [wedge.scad](./CGAL4All/wedge.scad)
- **Julia's** and **Mandelbrot's** fractals visualisations: [julia.py](./julia.py) and [mandelbrot.py](./mandelbrot.py)
### Varia
- an isomorphism in action: [ueola.py](./ueola.py)
