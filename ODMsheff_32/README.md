# SfM-MVS

[OpenDroneMap](https://github.com/OpenDroneMap/ODM) [Sheffield Park dataset number 3](https://github.com/pierotofy/drone_dataset_sheffield_park_3/tree/master)

[MvgMvsPipeline_ODMsheff_32.py](https://github.com/AdrianKriger/aerialPhotogrammetry101/blob/main/ODMsheff_32/MvgMvsPipeline_ODMsheff_32.py) will produce a sparse (SfM with [openMVG](https://github.com/openMVG/openMVG)) then dense (MVS with [openMVS](https://github.com/cdcseacave/openMVS)) reconstruction.


Good-to-know:
- The command is: `python MvgMvsPipeline_ODMsheff_32.py C:\{path to imagery}\images C:\{path to result}\result`. `cmd prompt` will ask where the camera parameters, openMVG and OpenMVS binaries are; or you can define the path [here](https://github.com/AdrianKriger/aerialPhotogrammetry101/blob/main/ODMsheff_32/MvgMvsPipeline_ODMsheff_32.py#L112-L118)
