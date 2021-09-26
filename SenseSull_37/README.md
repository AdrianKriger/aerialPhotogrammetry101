**[senseFly](https://www.sensefly.com/)** [Sullens](https://www.sensefly.com/education/datasets/?dataset=1420) ~ *37 oblique images*

`python MvgMvsPipeline_senseFly_37.py C:\{path to imagery}\images C:\{path to result}\result`  
will produce a sparse (SfM with [openMVG](https://github.com/openMVG/openMVG)) then dense (MVS with [openMVS](https://github.com/cdcseacave/openMVS)) reconstruction

Go Further:  *execute [sense37_Code.py](https://github.com/AdrianKriger/aerialPhotogrammetry101/blob/main/SenseSull_37/sense37_Code.py) through [sense37_Main.py](https://github.com/AdrianKriger/aerialPhotogrammetry101/blob/main/SenseSull_37/sense37_Main.py) with parameters from [params.json](https://github.com/AdrianKriger/aerialPhotogrammetry101/blob/main/SenseSull_37/params.json)*
- read the `scene_dense.ply` into a [PDAL](https://pdal.io/index.html#) pipeline and:
     - project to local coordinate system;
     - outlier detection;
     - ground filtering; and 
     - write `.las`
- create a terrain (dtm) and surface model (dsm) with the [AHN3 interpolation techniques](https://github.com/khalhoz/geo1101-ahn3-GF-and-Interpolation); that is:
    - dtm - with Laplace interpolation via Delaunay triangulation ([startin](https://github.com/hugoledoux/startinpy/)); and
    - dsm - with home-baked quadrant-based inverse-distance weighting 

 [sense37.ipynb](https://github.com/AdrianKriger/aerialPhotogrammetry101/blob/main/SenseMor_127/sense127.ipynb) for a look.

Good-to-know:
- [MvgMvsPipeline_senseFly_37.py](https://github.com/AdrianKriger/aerialPhotogrammetry101/blob/main/SenseSull_37/MvgMvsPipeline_senseFly_37.py):
    - will ask where the camera parameters, openMVG and openMVS binaries are; or you can define the path [here](https://github.com/AdrianKriger/aerialPhotogrammetry101/blob/main/SenseSull_37/MvgMvsPipeline_senseFly_37.py#L114-L120)
    - `-c ` ([cache](https://github.com/AdrianKriger/aerialPhotogrammetry101/blob/main/SenseMor_127/MvgMvsPipeline_senseFly_37.py#L216)) is limited to 100, dense reconstruction is harvested at 1/4 [resolution](https://github.com/AdrianKriger/aerialPhotogrammetry101/blob/main/SenseMor_127/MvgMvsPipeline_senseFly_37.py#L251).
- note the [crop](https://github.com/AdrianKriger/aerialPhotogrammetry101/blob/main/SenseSull_37/sense37_Code.py#L112-L115)
