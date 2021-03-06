# Applied Pythonology
![Laocoön and His Sons](https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/Laocoon_Pio-Clementino_Inv1059-1064-1067.jpg/250px-Laocoon_Pio-Clementino_Inv1059-1064-1067.jpg)
## Basic system identification and image processing (a.k.a. 'machine learning and machine vision') algorithms
### Low-level image processing
- basic interpolation: [interpolation1D.py](./interpolation1D.py) and [interpolation2D.py](./interpolation2D.py)
- simple scaling and rotation: [rotatioNN.py](./rotatioNN.py) and [rotation2D.py](./rotation2D.py)
- basic demosaicking (for Bayer and X-Trans CFAs): [demosaicking.py](./demosaicking.py) and [demosaickingX.py](./demosaickingX.py)
- low-light image generation: [Poissoning.py](./Poissoning.py)
- Monte Carlo pixel counting/area measurements: [MonteCarlo.py](./MonteCarlo.py)
- JPEG 'lite' algorithm: [jpglite.py](./jpglite.py)
- JPEG 2000 'featherlite' algorithm: [J2K.py](./J2K.py)  
- Julia and Mandelbrot fractals visualisations: [julia.py](./julia.py) and [mandelbrot.py](./mandelbrot.py)
- J. Duda's ANS compression: [ans.py](./ans.py)
### Modeling and identification
- basic pseudo-random number generator: [pseudogenerator.py](./pseudogenerator.py)
- basic function regression estimation with \emph{L2} cost function and \emph{Lq} constraints: [regressionCVX.py](./regressionCVX.py)
- Julia and Mandelbrot fractals (yes, again but now as the nonlinear dynamic phenomena): [julia.py](./julia.py) and [mandelbrot.py](./mandelbrot.py)
- Collatz conjecture visualization: [collatz.py](./collatz.py)
- Golden Section Search: [GSS.py](./GSS.py)
- Monty Hall's (no-)problem: [MontyHall.py](./montyhall.py)
### Todo(s)
- [ ] other simple image processing algorithms 
	- [ ] bilateral convolution filters
	- [ ] orthogonal series approximations and denoising
	- [ ] H.265-like compression schemes
	- [ ] contrast and phase-detection autofocusing models and algorithms
- [ ] other system identification algorithms
	- [ ] dedicated routines for Wiener and Hammerstein systems
	- [ ] Volterra and Wiener series based algorithms for more general structures (LNL, NLN, etc.)
- [ ] other modeling algorithms
	- [ ] Hidden Markov Model-based avatar behavior
