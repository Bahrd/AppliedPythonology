# Applied Pythonology
## System identification and image processing algorithms
### Low-level image processing
- basic interpolation algorithm: [interpolation.py](./interpolation.py)
- basic demosaicking (for Bayer and X-Trans CFAs) algorithms: [demosaicking.py](./demosaicking.py) and [demosaickingX.py](./demosaickingX.py)
- Julia and Mandelbrot fractals visualisations: [julia.py](./julia.py) and [mandelbrot.py](./mandelbrot.py)
### Modeling and identification
- basic pseudo-random number generator: [pseudogenerator.py](./pseudogenerator.py)
- basic function regression estimation with L1 constraints: [regressionCVX.py](./regressionCVX.py)
### Todo(s)
- [ ] other simple image processing algorithms 
	- [ ] orthogonal series approximations
	- [ ] JPG/H.264/5-like compression schemes
	- [ ] contrast and phase-detection AF algorithms
- [ ] other system identification algorithms
	- [ ] dedicated algorithms for Wiener and Hammerstein systems
	- [ ] Volterra and Wiener series based algorithms for more general structures (LNL, NLN, etc.)
- [ ] other modeling algorithms
	- [ ] Hidden Markov Model-based avatar behavior
	- [ ] video segmentation and anonimization
	- [ ] fatigue-controlled virtual window