# SfM-MVS

[senseFly](https://www.sensefly.com/) [Mormont quarry](https://www.sensefly.com/education/datasets/?dataset=1418) ~ **127 images**

`python [MvgMvsPipeline_ODMsheff_32.py](https://github.com/AdrianKriger/aerialPhotogrammetry101/blob/main/ODMsheff_32/MvgMvsPipeline_ODMsheff_32.py) C:\{path to imagery}\images C:\{path to result}\result` will produce and sparse (SfM with [openMVG](https://github.com/openMVG/openMVG)) then dense (MVS with [openMVS](https://github.com/cdcseacave/openMVS)) reconstruction

Go Further:  **execute [sense127_Code.py]() through [sense127_Main.py]() with parameters from [params.json]()**
- read the `scene_dense.ply` into a [PDAL](https://pdal.io/index.html#) pipeline and:
     - project to local coordinate system;
     - outlier detection;
     - ground filtering; and 
     - write `.las`
- create a digital terrain model with Laplace interpolation via Delaunay triangulation ([startin](https://github.com/hugoledoux/startinpy/))

 [sense127.ipynb]() for a look.

Good-to-know:
- [MvgMvsPipeline_ODMsheff_32.py](https://github.com/AdrianKriger/aerialPhotogrammetry101/blob/main/ODMsheff_32/MvgMvsPipeline_ODMsheff_32.py):
    - will ask where the camera parameters, openMVG and openMVS binaries are; or you can define the path [here](https://github.com/AdrianKriger/aerialPhotogrammetry101/blob/main/ODMsheff_32/MvgMvsPipeline_ODMsheff_32.py#L112-L118)'
    - [`cache`[() is limited to 100, dense recontruction is harvested at 1/4 resolution
