**[Pix4D](https://www.pix4d.com/)** [Echallens](https://support.pix4d.com/hc/en-us/articles/360000235126-Example-projects-real-photogrammetry-data#labelM2) ~ *100 images*

`python MvgMvsPipeline_Pix4D100.py C:\{path to imagery}\images C:\{path to result}\result`  
will produce a sparse (SfM with [openMVG](https://github.com/openMVG/openMVG)) then dense (MVS with [openMVS](https://github.com/cdcseacave/openMVS)) reconstruction

Go Further:  *execute [sense37_Code.py](https://github.com/AdrianKriger/aerialPhotogrammetry101/blob/main/Pix4Echa_100/pix4D100_Code.py) through [sense37_Main.py](https://github.com/AdrianKriger/aerialPhotogrammetry101/blob/main/Pix4Echa_100/pix4D100_Main.py) with parameters from [params.json](https://github.com/AdrianKriger/aerialPhotogrammetry101/blob/main/Pix4Echa_100/params.json)*
- read the `scene_dense.ply` into a [PDAL](https://pdal.io/index.html#) pipeline and:
     - project to local coordinate system;
     - outlier detection;
     - ground filtering; and 
     - write `.las`
- create a terrain (dtm) and surface model (dsm) with the prefered [AHN3 interpolation techniques](https://github.com/khalhoz/geo1101-ahn3-GF-and-Interpolation); that is:
    - dtm - with Laplace interpolation via Delaunay triangulation ([startin](https://github.com/hugoledoux/startinpy/)); and
    - dsm - with home-baked quadrant-based inverse-distance weighting 

 [pix4D100.ipynb](https://github.com/AdrianKriger/aerialPhotogrammetry101/blob/main/Pix4Echa_100/pix4D100.ipynb) for a look.

Good-to-know:
- [MvgMvsPipeline_Pix4d100100.py](https://github.com/AdrianKriger/aerialPhotogrammetry101/blob/main/Pix4Echa_100/MvgMvsPipeline_Pix4D100.py):
    - will ask where the camera parameters, openMVG and openMVS binaries are; or you can define the path [here](https://github.com/AdrianKriger/aerialPhotogrammetry101/blob/main/Pix4Echa_100/MvgMvsPipeline_Pix4D100.py#L114-L120)
    - `-c ` ([cache](https://github.com/AdrianKriger/aerialPhotogrammetry101/blob/main/Pix4Echa_100/MvgMvsPipeline_Pix4D100.py#L216)) is limited to 100, dense reconstruction is harvested at 1/4 [resolution](https://github.com/AdrianKriger/aerialPhotogrammetry101/blob/main/Pix4Echa_100/MvgMvsPipeline_Pix4D100.py#L251).
- note the [crop](https://github.com/AdrianKriger/aerialPhotogrammetry101/blob/main/Pix4Echa_100/pix4D100_Code.py#L116-L119)
