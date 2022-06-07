# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 20:41:28 2017

@author: Arslanova Linara
"""
from __future__ import print_function
import os
import pci.api as papi                      
import numpy as np
import fnmatch
from pci.api import datasource
from pci.mosprep import mosprep
from pci.mosdef import mosdef
from pci.mosrun import mosrun




def image_header_builder(file_name, image_sufix, new_folder_name, new_suffix, date_format):#'pix':
    '''
    function bild the new image name;
    <file_name> file name that must be used to build the new directory for the file; for example C:\data\irvine.pix
    <image_sufix> for import images from auxiliary files; use the sufix "-Thermal, - PAN", "- MS"
    '''
    new_link_directory = os.path.join(os.path.split(file_name)[0], new_folder_name)
    if not os.path.isdir(new_link_directory):
        os.mkdir(new_link_directory)
    image_name = os.path.join(new_link_directory, ".".join([os.path.basename(file_name).split(".", 1)[0].rsplit("_", 1)[0] + ("_" + str(image_sufix) + "_" +  new_suffix), date_format]))
    if os.path.exists(image_name):
        print("file already exist")
        os.remove(image_name)    # if you want to overwrite it
    return image_name


def load_image(filename, channel):
    ''' function to open the channels: channel number [1-7] '''
    with papi.datasource.open_dataset(filename) as ds: # channel = indicies.CHANNELS
        name = filename
        
        reader = papi.datasource.BasicReader(ds, range(1, len(channel)+1))                       
        in_coord_sys = reader.crs
        in_geocode = reader.geocoding
        in_raster = reader.read_raster(0, 0, reader.width, reader.height)
        return {
            'name': name,
            'reader': reader,
            'coords': in_coord_sys,
            'geocode': in_geocode,
            'raster': in_raster
        }
     

def split_channels(image, channel, data_type, no_value): #channel = indicies.CHANNELS, datatype = np.float32
    ''' function to convert numpy array (open channels)to 32bit float'''
    channels = {}
    for i, c in enumerate(channel):
        name = image['name'][i]
        orig = image['raster'].data[:,:, i]
        orig_masked  = np.ma.masked_equal(orig, no_value)
        flt = orig_masked.astype(data_type)
        channels[c] = flt
    return channels


def write_raster_to_file(index_raster, outname, DFORMAT, in_coord_sys, in_geocode):
    ''' function to write the output INDICIES (array) to raster object'''
    with papi.datasource.new_dataset(outname, DFORMAT, '') as write_dataset:
        writer = papi.datasource.BasicWriter(write_dataset)
        # Define file dimensions and write pixel values to file
        writer.create(index_raster)
        writer.write_raster(index_raster)
        # Add coordinate system and geocoding to output file
        writer.crs = in_coord_sys         
        writer.geocoding = in_geocode     


### mask_value could be token from the document:
### https://landsat.usgs.gov/sites/default/files/documents/lasrc_product_guide.pdf
        
@np.vectorize
def find_value(mask_value):
    ''' function to extract cloud and water body mask'''
    if mask_value == 352 or mask_value == 368 or  mask_value == 416 or  mask_value == 432 or  mask_value == 480 or  mask_value == 864 or  mask_value == 880 or  mask_value == 928 or  mask_value == 944 or  mask_value == 992 or  mask_value == 324 or  mask_value == 388 or  mask_value == 836 or  mask_value == 900 or  mask_value == 134:
        return 100
    else:
        return 0  


def create_bitmap_mask(filename, decision_value):
    ''' function to write extracted mask from "find_value function to new file" '''
    with papi.datasource.open_dataset(filename, papi.datasource.eAM_WRITE) as ds:
        name = filename
        reader = papi.datasource.BasicReader(ds, [1])                       
        in_raster = reader.read_raster(0, 0, reader.width, reader.height)
        decision = papi.gobs.BkgdMaskerSingleVal(decision_value, papi.gobs.BkgdRule.ALL_CHAN)
        builder = papi.gobs.DecisionMaskBuilder(decision)
        in_mask = builder.build_mask(in_raster)
        ds.write_mask(in_mask)



def find_file(working_dir, patter1, daten_format1, pattern2, datenformat2, output_folder):
    ''' function to find file with defined pattern
        returns a dictionary '''
    all_input_paths = {}
    for folder in os.listdir(working_dir):
        root = os.path.join(working_dir, folder, output_folder)
        if not os.path.isdir(root):
            os.mkdir(root)
        directory = os.listdir(root)
        for pix_file in fnmatch.filter(directory, ('*' + patter1 + '.' +  daten_format1)):
            for  mask_file in fnmatch.filter(directory, ('*' + pattern2 + '.' +  datenformat2)):
                all_input_paths[os.path.join(root, pix_file)] = os.path.join(root, mask_file)
    return all_input_paths


def group(lst, n):
    ''' function to split a list into groups'''
    for i in range(0, len(lst), n):
        val = lst[i:i+n]
        if len(val) == n:
            yield tuple(val)


def mosaic_images(directory_input_file, output_dir_mosaic, new_file_name_mosprep,  new_file_name_mosdef, NORMALIZE, BALSPEC, CUTMTHD, SORTMTHD, no_value, pattern):
    ''' function to generate full resolution mosaic'''
    mosprep(mfile = directory_input_file, silfile = new_file_name_mosprep, nodatval=[no_value], sortmthd = SORTMTHD, normaliz = NORMALIZE, balspec = BALSPEC , loclmask= "", globfile="", globmask=[], cutmthd = CUTMTHD)
    mosdef(silfile = new_file_name_mosprep, mdfile = new_file_name_mosdef, dbic = [], tispec = '', tipostrn = '', mapunits = '', pxszout = [], blend = [] , nodatval = [no_value], ftype = pattern, foptions = '')
    mosrun(silfile = new_file_name_mosprep, mdfile = new_file_name_mosdef, outdir = output_dir_mosaic, tilist = '' , crsrcmap = '' , extirule = '', delempti = '', proc = '', resample = '')



