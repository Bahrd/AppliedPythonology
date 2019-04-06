![Python programming allegory](https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/Laocoon_Pio-Clementino_Inv1059-1064-1067.jpg/250px-Laocoon_Pio-Clementino_Inv1059-1064-1067.jpg)
# Applied Pythonology
## System identification and image processing algorithms
### Low-level image processing
- basic interpolation algorithm: [interpolation.py](./interpolation.py)
- basic demosaicking (for Bayer and X-Trans CFAs) algorithms: [demosaicking.py](./demosaicking.py) and [demosaickingX.py](./demosaickingX.py)
- JPG 'lite" compression scheme: [jpglite.py](./jpglite.py)
- Julia and Mandelbrot fractals visualisations: [julia.py](./julia.py) and [mandelbrot.py](./mandelbrot.py)
### Modeling and identification
- basic pseudo-random number generator: [pseudogenerator.py](./pseudogenerator.py)
- basic function regression estimation with Lq constraints: [regressionCVX.py](./regressionCVX.py)
### Todo(s)
- [ ] other simple image processing algorithms 
	- [ ] orthogonal series approximations and denoising
	- [ ] JPEG 2000 and H.265-like compression schemes
	- [ ] contrast and phase-detection autofocusing
- [ ] other system identification algorithms
	- [ ] dedicated algorithms for Wiener and Hammerstein systems
	- [ ] Volterra and Wiener series based algorithms for more general structures (LNL, NLN, etc.)
- [ ] other modeling algorithms
	- [ ] Hidden Markov Model-based avatar behavior
	- [ ] video anonimization and semantic segmentation
	- [ ] fatigue-controlled virtual window