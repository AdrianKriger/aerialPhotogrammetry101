# -*- coding: utf-8 -*-
# env/ANH3


# author: arkriger
# https://github.com/AdrianKriger/aerialPhotogrammetry101/tree/main/SenseMor_127

import math
import json
import numpy as np
import pandas as pd
from laspy.file import File

import pdal

def get_ply(fpath, jparams):#, gnd_only = False):
    """Takes the filepath to an input ply file and the
    desired output raster cell size. Reads the ply file, performs basic cleaning, 
    reprojects, ground filtering, transforms to a 
    .las and outputs the ground points as a numpy array. 
    Also establishes some basic raster parameters:
        - the extents
        - the resolution in coordinates
        - the coordinate location of the relative origin (bottom left)
    """
    
    #Import LAS into numpy array 
    array = clsy_pipe(fpath, jparams)
    lidar_points = np.array((array['X'], array['Y'], array['Z'])).transpose()
    
    #Transform to pandas DataFrame
    lidar_df = pd.DataFrame(lidar_points, columns=['x', 'y', 'z'])
    extent = [[lidar_df.x.min(), lidar_df.x.max()],
              [lidar_df.y.min(), lidar_df.y.max()]]
    res = [math.ceil((extent[0][1] - extent[0][0]) / jparams["size"]),
           math.ceil((extent[1][1] - extent[1][0]) / jparams["size"])]
    origin = [np.mean(extent[0]) - (jparams["size"] / 2) * res[0],
              np.mean(extent[1]) - (jparams["size"] / 2) * res[1]]
    ul_origin = [np.mean(extent[0]) - (jparams["size"] / 2) * res[0],
                 np.mean(extent[1]) + (jparams["size"] / 2) * res[1]]
    
    # if gnd_only == True:
    #     array = array[(array['Classification'] == 2) & (array['Classification'] != 7)]
    #     #in_np = np.vstack((ground['X'], ground['Y'], ground['Z'])).T
    # else:
    #     # don't .T here. 
    #     # ~ .T inside the various functions so that pdal_idw does not have to read the file
    #     array = array[array['Classification'] != 7]
        
    return array, res, origin, ul_origin

def clsy_pipe(ply, jparams):
    """
    pdal pipeline to read .las, poisson resample, identify low noise, identify outliers, 
    classify ground and non-ground 
    ~ refine the classification with a nearest neighbor search and write the result as a .las
    """
   
    pline={
        "pipeline": [
            {
                "type": "readers.ply",
                "filename": ply,
                "default_srs": "+proj=geocent +ellps=WGS84 +datum=WGS84 +no_defs"
            },
            {
                "type":"filters.sample",
                "radius": jparams['thinning-factor']
            },
            {
                "type":"filters.reprojection",
                "in_srs":"+proj=geocent +ellps=WGS84 +datum=WGS84 +no_defs",
                "out_srs": jparams['crs']
            },
            {
                "type":"filters.elm"
            },
            {
                "type":"filters.outlier",
                "method":"statistical",
                "mean_k": 12,
                "multiplier": 1.2
            },
            {
                "type":"filters.pmf",
                #"slope": jparams["gf-angle"],
                "ignore":"Classification[7:7]",
                "initial_distance": jparams['initial_distance'],
                "max_distance": jparams['max_distance'],
                "max_window_size": jparams['initial_distance'] + 20
            },
            {
                "type":"filters.range",
                "limits":"Classification[1:2]"
            },
            # {
            #     "type" : "filters.neighborclassifier",
            #     "domain" : "Classification[2:2]",
            #     "k" : 7
            # },
            # {
            #      "type": "filters.approximatecoplanar",
            #      "knn": 10
            # },
            # {
            #     "type":"filters.estimaterank",
            # },
            {
                "type":"writers.las",
                "filename": jparams['out-las']
            }
            # {
            #     "type":"filters.crop",
            #     "bounds": jparams['bounds']
            # }

          ]
        } 
    
    pipeline = pdal.Pipeline(json.dumps(pline))
    #pipeline.validate() 
    count = pipeline.execute()
    array = pipeline.arrays[0]
    
    return array

def execute_startin(array, res, origin, size, method):
    """Takes the grid parameters and the ground points. Interpolates
    either using the TIN-linear or the Laplace method. Uses a
    -9999 no-data value. Fully based on the startin package.
    """
    import startinpy
    
    array = array[(array['Classification'] == 2) & (array['Classification'] != 7)]#\
                  #& (array['Coplanar'] != 0) & (array['Rank'] != 3)]
    pts = np.vstack((array['X'], array['Y'], array['Z'])).T
    tin = startinpy.DT(); tin.insert(pts)
    ras = np.zeros([res[1], res[0]])
    if method == 'startin-TINlinear':
        def interpolant(x, y): return tin.interpolate_tin_linear(x, y)
    elif method == 'startin-Laplace':
        def interpolant(x, y): return tin.interpolate_laplace(x, y)
    yi = 0
    for y in np.arange(origin[1], origin[1] + res[1] * size, size):
        xi = 0
        for x in np.arange(origin[0], origin[0] + res[0] * size, size):
            tri = tin.locate(x, y)
            if tri != [] and 0 not in tri:
                ras[yi, xi] = interpolant(x, y)
            else: ras[yi, xi] = -9999
            xi += 1
        yi += 1
    return ras, tin


def execute_idwquad(array, res, origin, size,
                    start_rk, pwr, minp, incr_rk, method, tolerance, maxiter):
    """Creates a KD-tree representation of the tile's points and
    executes a quadrant-based IDW algorithm on them. Although the
    KD-tree is based on a C implementation, the rest is coded in
    pure Python (below). Keep in mind that because of this, this
    is inevitably slower than the rest of the algorithms here.
    To optimise performance, one is advised to fine-tune the
    parametrisation, especially tolerance and maxiter.
    """
    from scipy.spatial import cKDTree
    
    array = array[array['Classification'] != 7]
    #array = array[(array['Classification'] == 1) & (array['Classification'] == 2)]
    pts = np.vstack((array['X'], array['Y'], array['Z'])).T
    ras = np.zeros([res[1], res[0]])
    tree = cKDTree(np.array([pts[:,0], pts[:,1]]).transpose())
    yi = 0
    for y in np.arange(origin[1], origin[1] + res[1] * size, size):
        xi = 0
        for x in np.arange(origin[0], origin[0] + res[0] * size, size):
            done, i, rk = False, 0, start_rk
            while done == False:
                if method == "radial":
                    ix = tree.query_ball_point([x, y], rk, tolerance)
                elif method == "k-nearest":
                    ix = tree.query([x, y], rk, tolerance)[1]
                xyp = pts[ix]
                qs = [
                        xyp[(xyp[:,0] < x) & (xyp[:,1] < y)],
                        xyp[(xyp[:,0] > x) & (xyp[:,1] < y)],
                        xyp[(xyp[:,0] < x) & (xyp[:,1] > y)],
                        xyp[(xyp[:,0] > x) & (xyp[:,1] > y)]
                     ]
                if min(qs[0].size, qs[1].size,
                       qs[2].size, qs[3].size) >= minp: done = True
                elif i == maxiter:
                    ras[yi, xi] = -9999; break
                rk += incr_rk; i += 1
            else:
                asum, bsum = 0, 0
                for pt in xyp:
                    dst = np.sqrt((x - pt[0])**2 + (y - pt[1])**2)
                    u, w = pt[2], 1 / dst ** pwr
                    asum += u * w; bsum += w
                    ras[yi, xi] = asum / bsum
            xi += 1
        yi += 1
    return ras

def write_geotiff(raster, origin, size, crs, fpath):
    """Writes the interpolated TIN-linear and Laplace rasters
    to disk using the GeoTIFF format. The header is based on
    the raster array and a manual definition of the coordinate
    system and an identity affine transform.
    """
    import rasterio
    from rasterio.transform import Affine
    transform = (Affine.translation(origin[0], origin[1])
                 * Affine.scale(size, size))
    #raster  = np.flip(raster, 0)
    with rasterio.Env():
        with rasterio.open(fpath, 'w', driver = 'GTiff',
                           height = raster.shape[0],
                           width = raster.shape[1],
                           count = 1,
                           dtype = rasterio.float32,
                           crs = crs,
                           #crs = '+proj=utm +zone=3 +ellps=WGS84 +datum=WGS84 +units=m +no_defs',
                           transform = transform
                           ) as out_file:
            out_file.write(raster.astype(rasterio.float32), 1)

def pdal_idw(array, res, origin, name, jparams):
    """Sets up a PDAL pipeline that reads a ground filtered LAS
    file, and writes it via GDAL. The GDAL writer has interpolation
    options, exposing the radius, power and a fallback kernel width
    to be configured. More about these in the readme on GitHub.
    """
    import pdal
    pline={
        "pipeline": [
            {
                "type":"writers.gdal",
                "filename": jparams['dtm_dsm'] + name + '_idwPDAL.tif',
                "resolution": jparams['size'],
                "radius": jparams['pdal-idw-rad'],
                "power": jparams['pdal-idw-pow'],
                "window_size": jparams['pdal-idw-wnd'],
                "output_type": "idw",
                "nodata": -9999,
                "dimension": "Z",
                "origin_x":  origin[0],
                "origin_y":  origin[1],
                "width":  res[0],
                "height": res[1]
            },
          ]
        } 
    
    p = pdal.Pipeline(json.dumps(pline), [array])
    #pipeline.validate() 
    p.execute()    
            
