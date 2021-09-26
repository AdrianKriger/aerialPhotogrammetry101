**[senseFly](https://www.sensefly.com/)** [Mormont quarry](https://www.sensefly.com/education/datasets/?dataset=1418) ~ *127 images*

`python MvgMvsPipeline_senseFly_127.py C:\{path to imagery}\images C:\{path to result}\result`  
will produce a sparse (SfM with [openMVG](https://github.com/openMVG/openMVG)) then dense (MVS with [openMVS](https://github.com/cdcseacave/openMVS)) reconstruction

Go Further:  *execute [sense127_Code.py](https://github.com/AdrianKriger/aerialPhotogrammetry101/blob/main/SenseMor_127/sense127_Code.py) through [sense127_Main.py](https://github.com/AdrianKriger/aerialPhotogrammetry101/blob/main/SenseMor_127/sense127_Main.py) with parameters from [params.json](https://github.com/AdrianKriger/aerialPhotogrammetry101/blob/main/SenseMor_127/params.json)*
- read the `scene_dense.ply` into a [PDAL](https://pdal.io/index.html#) pipeline and:
     - project to local coordinate system;
     - outlier detection;
     - ground filtering; and 
     - write `.las`
- create a digital terrain model with Laplace interpolation via Delaunay triangulation ([startin](https://github.com/hugoledoux/startinpy/))

 [sense127.ipynb](https://github.com/AdrianKriger/aerialPhotogrammetry101/blob/main/SenseMor_127/sense127.ipynb) for a look.

Good-to-know:
- [MvgMvsPipeline_senseFly_127.py](https://github.com/AdrianKriger/aerialPhotogrammetry101/blob/main/SenseMor_127/MvgMvsPipeline_senseFly_127.py):
    - will ask where the camera parameters, openMVG and openMVS binaries are; or you can define the path [here](https://github.com/AdrianKriger/aerialPhotogrammetry101/blob/main/SenseMor_127/MvgMvsPipeline_senseFly_127.py#L116-L121)
    - `-c ` ([cache](https://github.com/AdrianKriger/aerialPhotogrammetry101/blob/main/SenseMor_127/MvgMvsPipeline_senseFly_127.py#L216)) is limited to 100, dense reconstruction is harvested at 1/4 [resolution](https://github.com/AdrianKriger/aerialPhotogrammetry101/blob/main/SenseMor_127/MvgMvsPipeline_senseFly_127.py#L251).
