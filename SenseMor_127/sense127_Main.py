# -*- coding: utf-8 -*-
# env/AHN3

#author: arkriger

# - takes the .ply and executes sense127_Code.py; that is:
# - enter PDAL pipeline (project from ecef geocentric to utm, outlier removal, 
#                        ground filtering - crop)
# - write .las
# - AHN3 dtm and dsm procedure: (https://github.com/khalhoz/geo1101-ahn3-GF-and-Interpolation) 
#     - dtm: delaunay triangulation with laplace interpolation(startin);
#     - dsm: quad-based idw
#

import os 
import glob
import json
import numpy as np
from pathlib import Path

import startinpy
#import rasterio

import time
from datetime import timedelta

from sense127_Code import execute_startin, get_ply, execute_idwquad, write_geotiff, pdal_idw

def main():
       
    start = time.time()
    
    jparams = json.load(open('params.json'))
    
    #-- make a .las folder
    path = os.getcwd()
    # Joins the folder that we wanted to create
    folder_name = 'result_utm/las/'
    path = os.path.join(path, folder_name) 
    # Creates the folder, and checks if it is created or not.
    os.makedirs(path, exist_ok=True)
    
    infile = jparams["input-ply"]
    array, res, origin, ul_origin = get_ply(infile, jparams)
    
    if jparams["dtm"] == "True":
        name = Path(infile).stem + '_dtm'
        
        rasLap, tinLap = execute_startin(array, res, origin, jparams["size"], 
                                         method='startin-Laplace')
        write_geotiff(rasLap, origin, jparams["size"], jparams["crs"], jparams["dtm_dsm"] + name + '_tinLaplace.tif')
        tinLap.write_obj(jparams["dtm_dsm"] + name + '_TINlaplace.obj')
        
    # if jparams["dsm"] == "True":
    #     name = Path(infile).stem + '_dsm'
        
    #     ras = execute_idwquad(array, res, origin, jparams["size"],
    #                           jparams["start_rk"], jparams["pwr"], jparams["minp"], 
    #                           jparams["incr_rk"], jparams["method"], jparams["tolerance"], 
    #                           jparams["maxiter"])
    #     write_geotiff(ras, origin, jparams["size"], jparams["crs"], jparams["dtm_dsm"] + name + '_idwQUAD.tif')
        
        #array = array[array['Classification'] != 7]
        #pdal_idw(array, res, origin, name, jparams)
        
    #-- timeit
    end = time.time()
    print('runtime:', str(timedelta(seconds=(end - start))))
    
    # ~~ runtime: 0:01:48.251903

    
if __name__ == "__main__":
    main()
    
    