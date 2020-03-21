# Applied Pythonology
![Laocoön and His Sons](https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/Laocoon_Pio-Clementino_Inv1059-1064-1067.jpg/250px-Laocoon_Pio-Clementino_Inv1059-1064-1067.jpg)
## System identification and image processing algorithms
### Low-level image processing
- basic interpolation algorithms: [interpolation1D.py](./interpolation1D.py) and [interpolation2D.py](./interpolation2D.py)
- simple scaling and rotation algorithms [rotationNN.py](./rotationNN.py) and [rotation2D.py](./rotation2D.py)
- basic demosaicking (for Bayer and X-Trans CFAs) algorithms: [demosaicking.py](./demosaicking.py) and [demosaickingX.py](./demosaickingX.py)
- JPG 'lite" compression scheme: [jpglite.py](./jpglite.py)
- Julia and Mandelbrot fractals visualisations: [julia.py](./julia.py) and [mandelbrot.py](./mandelbrot.py)
- J. Duda's ANS compression scheme: [ans.py](./ans.py)
### Modeling and identification
- basic pseudo-random number generator: [pseudogenerator.py](./pseudogenerator.py)
- basic function regression estimation with Lq constraints: [regressionCVX.py](./regressionCVX.py)
- Julia and Mandelbrot fractals (yes, again but now as the nonlinear dynamic phenomena): [julia.py](./julia.py) and [mandelbrot.py](./mandelbrot.py)
- Collatz conjecture visualization: [collatz.py](./collatz.py)
### Todo(s)
- [ ] other simple image processing algorithms 
	- [ ] bilateral convolution filters
	- [ ] orthogonal series approximations and denoising
	- [ ] JPEG 2000 and H.265-like compression schemes
	- [ ] contrast and phase-detection autofocusing
- [ ] other system identification algorithms
	- [ ] dedicated routines for Wiener and Hammerstein systems
	- [ ] Volterra and Wiener series based algorithms for more general structures (LNL, NLN, etc.)
- [ ] other modeling algorithms
	- [ ] Hidden Markov Model-based avatar behavior
