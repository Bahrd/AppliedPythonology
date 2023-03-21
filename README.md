# Applied Pythonology
![Laocoön and His Sons](https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/Laocoon_Pio-Clementino_Inv1059-1064-1067.jpg/250px-Laocoon_Pio-Clementino_Inv1059-1064-1067.jpg)
## Basic system identification and image processing (a.k.a. 'machine learning and machine vision') algorithms
### Low-level image and data processing
- basic interpolation
  - 1D: [interpolation1D.ipynb](./interpolation1D.ipynb) & [interpolation1D.py](./interpolation1D.py)
  - 2D: [interpolation2D.py](./interpolation2D.py)
- simple scaling and rotation: [rotatioNN.py](./rotatioNN.py) and [rotation2D.py](./rotation2D.py)
- basic demosaicking (for Bayer and X-Trans® CFAs): [demosaicking.py](./demosaicking.py) and [demosaickingX.py](./demosaickingX.py)
- low-light image generation: [Poissoning.py](./Poissoning.py)
- Monte Carlo pixel counting/area measurements: [MonteCarlo.py](./MonteCarlo.py)
- JPEG 'lite' algorithm: [jpglite.py](./jpglite.py)
- JPEG 2000 'featherlite' algorithm: [J2K.py](./J2K.py)
- wavelet thresholding families: [WaveletThresholding.py](./WaveletThresholding.py)
- Julia's and Mandelbrot's fractals visualisations: [julia.py](./julia.py) and [mandelbrot.py](./mandelbrot.py)
- J\. Duda's ANS compression coding: [ans.py](./ans.py)
- Hamming code: [HammingBird.ipynb](./HammingBird.ipynb) and [HammingBird.py](./HammingBird.py)
### Modeling and identification
- basic pseudo-random number generator: [pseudogenerator.py](./pseudogenerator.py)
- basic function regression estimation with _L<sub>2</sub>_ cost function and _L<sub>q</sub>_ constraints: [regressionCVX.py](./regressionCVX.py)
- Julia's and Mandelbrot's fractals (yes, again but now as a nonlinear dynamic phenomena): [julia.py](./julia.py) and [mandelbrot.py](./mandelbrot.py)
- Collatz's conjecture visualization: [collatz.py](./collatz.py)
- Golden Section Search: [GSS.py](./GSS.py)
- Monty Hall's (no-)problem: [MontyHall.py](./montyhall.py)
### Todo(s)
- [ ] other simple image processing algorithms
	- [ ] bilateral convolution filters
	- [ ] H.265-like video compression schemes
	- [ ] contrast and phase-detection autofocusing models and algorithms
- [ ] other system identification algorithms
	- [ ] dedicated routines for Wiener and Hammerstein systems
	- [ ] Volterra and Wiener series based algorithms (for more general structures (LNL, NLN, etc.): see [Sz. Łagosz's Entropic-Dual-Averaging algorithm](https://github.com/slagosz/Entropic-Dual-Averaging))
- [ ] other modeling algorithms
	- [ ] Hidden Markov Model-based avatar behavior
