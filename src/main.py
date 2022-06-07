import os                                   
import fnmatch
import re
import shutil
import inspect
import datetime
import numpy as np
from pci.api import gobs
from pci.fimport import fimport
from pci.burnmask import burnmask
from pci.iii import iii 
from pci.pcimod import pcimod
from pci.link import link

from pci.exceptions import PCIException


import utils
import indicies





# --- Definition of constants 
TIF_PATTERN = 'tif'
MS_PATTERN = 'MS'
XML_PATTERN = 'xml'
PIX_PATTERN =  'pix'
PIXQA_PATTERN ='_pixel_qa'
BAND_PATTERN = 'band'
INDEX_FOLDER = 'Veg_Indices'
MOSAIC_FOLDER = 'Mosaic_sets'
FULL_MOSAIC_FOLDER = "full_image_mosaic"
OUTPUT_FOLDER = "output"
MASK_SUFFIX = 'mask'
RMCLOUD_SUFFIX = 'rmCloud'
ORIG_SUFFIX = 'orig'
MOSPREP_SUFFIX = 'mosprep'
MOSDEF_SUFFIX = 'mosdef'
QABAND_SUFFIX = "qab"
NO_VALUE = -9999
L8_REPEAT_CYCLE = raw_input("Please give the number that represent maximum difference \nbetween two image acquisition dates. \nStandart number is 17. This is required for mosaicing two paths.  ")


import locale
locale.setlocale(locale.LC_ALL, "")
locale.setlocale(locale.LC_NUMERIC, "C")
       


def main():
    
    print("-" * 80)
    print(" 1. setting the working directory...")
    print("-" * 80)
    
    working_dir = raw_input("Please state your input folder path: ")
    # --- define variable to create a new dirrctory name 
    new_dir_mosaic = os.path.join(working_dir, MOSAIC_FOLDER)
    new_dir_index = os.path.join(working_dir, INDEX_FOLDER)
    
    #--- load the index formeln from modul formel.py   
    name_func_tuples = inspect.getmembers(indicies, inspect.isfunction)
    frm = dict(name_func_tuples)
    
    ### breaking points for processing with NO  
    DECISION1 = raw_input("Should be channels stacked (YES/NO):  ")
    DECISION2 = raw_input("Should be mask extracted  (YES/NO):   ")
    DECISION3 = raw_input("Should be mask burned into raster (YES/NO):   ")
    DECISION4 = raw_input("Should be image set mosaicked (YES/NO):   ")
    DECISION5 = raw_input("Should be index calculated (YES/NO):   ")
    DECISION6 = raw_input("Should be index image mosaicked (YES/NO):   ")
    DECISION7 = raw_input("Should be full image mosaicking performed (YES/NO):   ")
    
    
    if DECISION1 == "YES":
        
        print("-" * 80)
        print(" 2. Channel stacking ...")
        print("-" * 80)
        
        all_bands = []
        # --- import image channels in to .pix (PCIDISK) format 
        for folder in os.listdir(working_dir):
            folder_path  = os.path.join(working_dir, folder)
            if not os.path.isdir(new_dir_mosaic):
                for bands in fnmatch.filter(os.listdir(folder_path), ('*' + BAND_PATTERN + '*')):
                    all_bands.append(bands)
                if len(all_bands) != 0:
                    in_file = os.path.join(folder_path, all_bands[0])
                    new_link_directory = os.path.join(folder_path, OUTPUT_FOLDER)
                    if not os.path.isdir(new_link_directory):
                        os.mkdir(new_link_directory)
                    pix_ms = os.path.join(new_link_directory, ".".join([os.path.basename(in_file).rsplit("_", 1)[0].rsplit("_", 1)[0] + ("_" + ORIG_SUFFIX), PIX_PATTERN]))
                    if os.path.exists(pix_ms):
                        print("file already exist and will be overwritten")
                        os.remove(pix_ms) 
                    #pix_ms = utils.image_header_builder(in_file,  MS_PATTERN, OUTPUT_FOLDER, ORIG_SUFFIX, PIX_PATTERN)
                    DBLAYOUT = "BAND"
                    fimport(fili = in_file, filo = pix_ms, dbiw = [], poption = 'OFF', dblayout = DBLAYOUT) #poption = "" - the function applies nearest-neighbor resampling;  
                    pcimod(pix_ms, "ADD", [0, 6, 0, 0, 0, 0])
                    print"start channel stacking for the image: %s" % (os.path.basename(pix_ms))
                    for i in range(1, len(all_bands)):
                        print "channel %s was imported" % (i+1)
                        in_bands = os.path.join(folder_path, all_bands[i])
                        iii(fili = in_bands , filo = pix_ms, dbic = [1], dboc = [i+1] , dbiw = [], dbow =[] )
                    print ("-" * 80)
                    all_bands[:] = []  
                else:
                    print("channels was not found" )        
    elif DECISION1 == "NO":
        pass
   
    
        
    all_input_paths = {}
    # --- organise images into dictionary
    for folder in os.listdir(working_dir):
        folder_path  = os.path.join(working_dir, folder)
        folder_path2 = os.path.join(folder_path, OUTPUT_FOLDER)
        if not os.path.isdir(folder_path2):
            os.mkdir(folder_path2)
        dir1= os.listdir(folder_path)
        dir2 = os.listdir(folder_path2)
        for pix_file in fnmatch.filter(dir2, ('*' + ORIG_SUFFIX + '.' +  PIX_PATTERN)):
            for  mask_file in fnmatch.filter(dir1, ('*' + PIXQA_PATTERN + '.' +  TIF_PATTERN)):
                all_input_paths[os.path.join(folder_path, pix_file)] = os.path.join(folder_path, mask_file)


    if DECISION2 == "YES":

        print("-" * 80)
        print(" 3. Extracting water and cloud mask from QA band...")
        print("-" * 80)

        all_input_paths2 = {}
        # ---  extract mask from _sr_pixel_ band
        for idx, (pix_file, mask_file) in enumerate(all_input_paths.items()): 
            print "(%d/%d) found valid input file: %s" % (idx+1, len(all_input_paths), mask_file) 
            ### import image data to .pix format 
            pix_ms = utils.image_header_builder(pix_file,  MS_PATTERN, OUTPUT_FOLDER, QABAND_SUFFIX, PIX_PATTERN)
            DBLAYOUT = "BAND"
            link(fili = mask_file, filo = pix_ms, dbiw = [])
            image = utils.load_image(pix_ms, [1])
            mask = utils.split_channels(image, [1], np.uint16, 1)
            for mask in mask.values():
                with np.errstate(invalid='ignore'):
                    array = utils.find_value(mask)
                    array_int = array.astype(np.uint8)
                    index_raster =  gobs.array_to_raster(array_int)
                    mask_ms = utils.image_header_builder(image['name'], "", "", MASK_SUFFIX, PIX_PATTERN)
                    utils.write_raster_to_file(index_raster, mask_ms, PIX_PATTERN, image['coords'], image['geocode'])       
                    utils.create_bitmap_mask(mask_ms, 0)
                    new_pix_file = os.path.join(os.path.dirname(pix_file),OUTPUT_FOLDER, os.path.basename(pix_file))
                    all_input_paths2[new_pix_file] = mask_ms
    elif DECISION2 == "NO":
         # --- to start workflow without channel stacking and mask exstracting
        all_input_paths2 = utils.find_file(working_dir, ORIG_SUFFIX, PIX_PATTERN, MASK_SUFFIX, PIX_PATTERN, OUTPUT_FOLDER)
        pass


    
    if DECISION3 == "YES":
        
        print("-" * 80)
        print(" 4. Start burning masks into images...  ")
        print("-" * 80)
        
        all_input_paths3 = {}   
        # --- burn mask into raster image
        for idx, (pix_file, mask_file) in enumerate(all_input_paths2.items()):
            print "(%d/%d) found valid input file: %s" % (idx+1, len(all_input_paths2), pix_file)
            try:
                cloudrem_ms = utils.image_header_builder(pix_file,  MS_PATTERN, '', RMCLOUD_SUFFIX, PIX_PATTERN)
                CHANNELS_BM = [1,2,3,4,5,6,7]
                BURNVAL = [NO_VALUE]
                burnmask(fili = pix_file, dbic = CHANNELS_BM, mask=[2], maskfile = mask_file, burnval = BURNVAL, filo = cloudrem_ms, dboc = CHANNELS_BM, ftype =  '', foptions = '')
                print('mask was burned...')
                all_input_paths3[pix_file] = cloudrem_ms
                
            except PCIException, e:
                print e
            except Exception, e:
                print

        print("")
        print(" mosaic was burned... ")
        print("" )

    elif DECISION3 == "NO":
         # --- to start workflow without channel stacking and mask exstracting
        all_input_paths3 = utils.find_file(working_dir, ORIG_SUFFIX, PIX_PATTERN, RMCLOUD_SUFFIX, PIX_PATTERN, OUTPUT_FOLDER)
        pass



    if DECISION4 == "YES":

        print("-" * 80)
        print(" 5. Creating new folders to store output-files after mosaicking...")
        print("-" * 80)

        directories_list = []
        folder_names_set = set()
        # --- creating folders for mosaicing 
        if len(all_input_paths3) > 1:
            for idx, (pix_file, mask_file) in enumerate(all_input_paths3.items()): 
                ### create folder names for each mosaicing set 
                file_name = ((os.path.basename(pix_file).rsplit("_", 3)[0]).split("_", 3)[3])
                path_name = os.path.basename(pix_file).split('_', 3)[2]
                path = str(path_name[0:3])
                folder_names_set.add(path +  '_' + file_name)
            folder_names_list = sorted(list(folder_names_set))
            for folder_images in folder_names_list:
                new_directory = os.path.join(new_dir_mosaic, folder_images)
                if not os.path.isdir(new_directory):
                    os.makedirs(new_directory)
                directories_list.append(new_directory)
                
        print("" )
        print(" Finish creation of folders...  ")
        print("" )


        print("-" * 80)
        print(" 6. Start image mosaicking")
        print("-" * 80)

        # --- copy the .pix file in folder for mosaicking sorting after image asqisition date
        for idx, (pix_file, rm_mask_file) in enumerate(all_input_paths3.items()):
            print "(%d/%d) found valid input file: %s" % (idx+1, len(all_input_paths3), pix_file)
            for value in directories_list:
                mask_file = os.path.basename(rm_mask_file)
                path_pattern = re.escape(os.path.basename(value).split('_', 1)[0])
                date_pattern = re.escape(os.path.basename(value).split('_', 1)[1])
                pattern = re.compile((r'.*' + str(path_pattern) + r'.*'  + str(date_pattern) + r'.*'))
                if(pattern.search(value)) and (pattern.search(mask_file)):
                    if not os.path.exists(os.path.join(value, mask_file)):
                        shutil.copy2(rm_mask_file, value)  # or shutil.move
                        print("image was moved:  ", os.path.basename(rm_mask_file))  
        # --- mosaic preparation
        print("-" * 80)
        for value in directories_list:
            for images in fnmatch.filter(os.listdir(value),('*' + RMCLOUD_SUFFIX   + '.' + PIX_PATTERN)):
                print "found valid input image: %s" % (images)
                print "found valid folder: %s" % (value)
                new_file_name_mosprep = os.path.join(value, ".".join([(os.path.basename(value)+ '_' + MOSPREP_SUFFIX), XML_PATTERN]))
                NORMALIZE = "NONE"
                BALSPEC = 'BUNDLE'              # 'HISTOGRAMM' / 'BUNDLE' only for images from the one path 
                CUTMTHD = "MINSQDIFF"
                SORTMTHD = "NEARESTCENTER"
                new_file_name_mosdef = os.path.join(value, ".".join([(os.path.basename(value)+ '_' + MOSDEF_SUFFIX), XML_PATTERN]))
                if not os.path.exists(new_file_name_mosprep):
                    try:
                        ### authomatic color balncing
                        output_dir_mosaic = os.path.join(os.path.dirname(value), OUTPUT_FOLDER)
                        if not os.path.isdir(output_dir_mosaic):                           
                            os.mkdir(output_dir_mosaic)
                        utils.mosaic_images(value, output_dir_mosaic, new_file_name_mosprep,  new_file_name_mosdef, NORMALIZE, BALSPEC , CUTMTHD, SORTMTHD, NO_VALUE, PIX_PATTERN)
                    except PCIException, e:
                        print e
                    except Exception, e:
                        print
                else:
                    ("file already exist")
        print(" Image mosaicking was finished... ")
        print("")
    elif DECISION4 == "NO":
        pass
    

    print("-" * 80)
    print(" 7. Start calculation of indices... ")
    print("-" * 80)

    if os.path.exists(new_dir_mosaic):
        images_list = []
        # --- calculate of indicies
        output_dir_mosaic = os.path.join(new_dir_mosaic, OUTPUT_FOLDER)
        for images_mosdef in fnmatch.filter(os.listdir(output_dir_mosaic), '*' + MOSDEF_SUFFIX + '_1_1.' + PIX_PATTERN):
            ### open channels and convert them to 32 float
            images = os.path.join(output_dir_mosaic, images_mosdef)
            images_list.append(images)
    else:
        pass

    if DECISION5 == "YES":
        for idx, images in enumerate(images_list):
            print "(%d/%d) found valid input file: %s" % (idx+1, len(images_list), os.path.basename(images))
            image = utils.load_image(images, indicies.CHANNELS) 
            channels = utils.split_channels(image, indicies.CHANNELS, np.float32, NO_VALUE)
            filemap = (image, channels)
            # --- calculate indicies and write them to raster
            for fidx, (ind_name, func) in enumerate(frm.items()):
                print "executing function %s: %d/%d" % (ind_name, fidx+1, len(frm))       
                with np.errstate(divide='ignore', invalid='ignore'):
                    try:
                        output_dir = os.path.join(new_dir_index, ind_name)
                        if not os.path.isdir(output_dir):                          
                            os.makedirs(output_dir)
                        index_array = func(channels)                            
                        index_raster = gobs.copy_array_to_raster(index_array)
                        outname = utils.image_header_builder(image['name'], MS_PATTERN, output_dir, ind_name, TIF_PATTERN)
                        utils.write_raster_to_file(index_raster, outname, TIF_PATTERN, image['coords'], image['geocode'])
                        print("image_name:", image['name'])
                        print(os.path.basename(images))
                    except PCIException as e:
                        import traceback
                        print ('-'*80)
                        traceback.print_exc()
                        print ('-'*80)
        print("")
        print(" Index calculation was finished")
        print("")
    
    elif DECISION5 == "NO":
        pass
           
    # --- delete image mosaic folder (one path)
    if os.path.exists(new_dir_mosaic):
        print("folder exist and will be removed: " + new_dir_mosaic)
        shutil.rmtree(new_dir_mosaic)
    else:
        print("folder %s was seccuessfully removed" % (new_dir_mosaic))
    # ---


    

        
    if DECISION6 == "YES":
        
        print("-" * 80)
        print(" 8. Start mosaicking of two paths ...")
        print("-" * 80)


        new_dir_output = os.path.join(new_dir_index, OUTPUT_FOLDER)
        if not os.path.isdir(new_dir_output):
            os.mkdir(new_dir_output)

        dir_set= set()
        date_set = set()
        dir_list = []
           

        
        # --- to create folders for final mosaic of two paths
        for idx, images in enumerate(images_list):
            print "(%d/%d) found valid input file: %s" % (idx+1, len(images_list), os.path.basename(images))
            date_name = os.path.basename(images).split('_', 2)[1]
            date_set.add(date_name)
        date_list = sorted(list(date_set))
        for date in date_list:    
            for number in range(0, len(date_list)-1):
                last_number = date_list[number + 1]
                date_last = datetime.datetime.strptime(last_number, '%Y%m%d').date()
                first_number = date_list[number]                    
                date_previous = datetime.datetime.strptime(first_number, '%Y%m%d').date()
                day_difference = (date_last - date_previous)
                print("day_difference:", day_difference.days)
                if 0 < int(day_difference.days) < L8_REPEAT_CYCLE:
                    new_directory = os.path.join(new_dir_output, (str(first_number) + '_' + str(last_number)))
                    dir_set.add(new_directory)
                else:
                    print("day difference more than repeat cycle")         
        dir_lst = sorted(list(dir_set))               
        for  i in range (0, len(dir_lst)+1):
            if not i %2:
                if not os.path.isdir(dir_lst[i]):
                    os.mkdir(dir_lst[i])
                dir_list.append(dir_lst[i])

    

        
        print("-" * 80)
        for idx, images in enumerate(images_list):
            # --- to find and move the index files into new folders
            for fidx, (ind_name, func) in enumerate(frm.items()):
                print "(%d/%d) found valid input file: %s" % (fidx+1, len(frm.items()), ind_name)
                for value in dir_list:
                    value_directory = os.path.join(value, ind_name)
                    if not os.path.isdir(value_directory):
                        os.makedirs(value_directory)
                    for extension in (('*' + (os.path.basename(images).split('_', 2)[1])), ('*' + "_" + ind_name), ('*' + TIF_PATTERN)):
                        for indices in fnmatch.filter(os.listdir(os.path.join(new_dir_index, ind_name)), extension):         
                            pattern1 = re.escape(os.path.basename(value).split('_', 1)[0])
                            pattern2 = re.escape(os.path.basename(value).split('_', 1)[1])
                            pattern = re.compile((r'.*'  + str(pattern1) + r'.*' ) + r'|' +  (r'.*'  + str(pattern2)+  r'.*'))
                            if(pattern.search(indices)) and (pattern.search(value)):
                                if not os.path.exists(os.path.join(value_directory , indices)):
                                    shutil.move(os.path.join(new_dir_index, ind_name, indices), value_directory )
                    # --- mosaic preparation
                    for images in os.listdir(value_directory):
                        print "found valid input image: %s" % (images)
                        images = os.path.join(os.path.dirname(value_directory), images)
                        new_file_name_mosprep = os.path.join(value_directory, ".".join([(os.path.basename(value)+ '_' + ind_name + '_' + MOSPREP_SUFFIX), XML_PATTERN]))
                        NORMALIZE = "ADAPTIVE"
                        BALSPEC = 'BUNDLE'              # 'HISTOGRAMM'/ 'BUNDLE' only for images from the one path 
                        CUTMTHD = "MINSQDIFF"
                        SORTMTHD = "NEARESTCENTER"
                        new_file_name_mosdef = os.path.join(value_directory, ".".join([(os.path.basename(value)+ '_' + ind_name + '_' + MOSDEF_SUFFIX), XML_PATTERN]))
                        if not os.path.exists(new_file_name_mosprep):
                            ### authomatic color balncing
                            try:
                                output_dir_mosaic = os.path.join(os.path.dirname(value), OUTPUT_FOLDER, ind_name)
                                if not os.path.isdir(output_dir_mosaic):                           
                                    os.makedirs(output_dir_mosaic)
                                utils.mosaic_images(value_directory, output_dir_mosaic, new_file_name_mosprep,  new_file_name_mosdef, NORMALIZE, BALSPEC, CUTMTHD, SORTMTHD, float(NO_VALUE), TIF_PATTERN)
                            except PCIException, e:
                                print e
                            except Exception, e:
                                print
    elif DECISION6 == "NO":
            pass

    if DECISION7 == "YES":
        
        dir_set= set()
        date_set = set()
        dir_list = []

        mosaic_list = []

        
        directories_list = []
        folder_names_set = set()
        # --- creating folders for mosaicing 
        if len(all_input_paths3) > 1:
            for idx, (pix_file, rm_mask_file) in enumerate(all_input_paths3.items()):
                
                ### create folder names for each mosaicing set 
                file_name = ((os.path.basename(rm_mask_file).rsplit("_", 3)[0]).split("_", 4)[3])
                print(file_name )
                path_name = os.path.basename(rm_mask_file).split('_', 3)[2]
                print(path_name)
                path = str(path_name[0:3])
                folder_names_set.add(path +  '_' + file_name)
            folder_names_list = sorted(list(folder_names_set))

        for folder_name in folder_names_list:
            path = folder_name.split("_", 1)[0]
            date_name = folder_name.split("_", 1)[1]
            date_set.add(date_name)
        date_list = sorted(list(date_set))
        
        for date in date_list:
            print(date)
        
            for number in range(0, len(date_list)-1):
                last_number = date_list[number + 1]
                date_last = datetime.datetime.strptime(last_number, '%Y%m%d').date()
                first_number = date_list[number]                    
                date_previous = datetime.datetime.strptime(first_number, '%Y%m%d').date()
                day_difference = (date_last - date_previous)
                print("day_difference:", day_difference.days)
                if 0 < int(day_difference.days) < L8_REPEAT_CYCLE:
                    
                    new_directory_mosaic = os.path.join(working_dir, FULL_MOSAIC_FOLDER)
                    if not os.path.isdir(new_directory_mosaic):                           
                        os.makedirs(new_directory_mosaic)
                    new_directory = os.path.join(new_directory_mosaic, (str(first_number) + '_' + str(last_number)))
                    dir_set.add(new_directory)
                else:
                    print("day difference more than repeat cycle")         
        dir_lst = sorted(list(dir_set))               
        for  i in range (0, len(dir_lst)+1):
            if not i %2:
                if not os.path.isdir(dir_lst[i]):
                    os.mkdir(dir_lst[i])
                dir_list.append(dir_lst[i])




        for folder in dir_list:
            for idx, (pix_file, rm_mask_file) in enumerate(all_input_paths3.items()):
                print "(%d/%d) found valid input file: %s" % (idx+1, len(all_input_paths3), os.path.basename(rm_mask_file))
                img = os.path.basename(rm_mask_file)
                fold = os.path.basename(folder)
                pattern1 = re.escape(os.path.basename(fold).split('_', 1)[0])
                pattern2 = re.escape(os.path.basename(fold).split('_', 1)[1])
                pattern = re.compile((r'.*'  + str(pattern1) + r'.*' ) + r'|' +  (r'.*'  + str(pattern2)+  r'.*'))
                if(pattern.search(img)) and (pattern.search(fold)):
                    if not os.path.exists(os.path.join(new_directory_mosaic, img)):
                        shutil.copy2(rm_mask_file, folder)
             
            for images in os.listdir(new_directory_mosaic):
                print "found valid input image: %s" % (images)
                #images = os.path.join(os.path.dirname(new_directory_mosaic), images)
                new_file_name_mosprep = os.path.join(folder, ".".join([(os.path.basename(folder)+ '_' + MOSPREP_SUFFIX), XML_PATTERN]))
                NORMALIZE = "ADAPTIVE"
                BALSPEC = 'BUNDLE'              # 'HISTOGRAMM'/ 'BUNDLE' only for images from the one path 
                CUTMTHD = "MINSQDIFF"
                SORTMTHD = "NEARESTCENTER"
                new_file_name_mosdef = os.path.join(folder, ".".join([(os.path.basename(folder)+ '_' + MOSDEF_SUFFIX), XML_PATTERN]))
                if not os.path.exists(new_file_name_mosprep):
                    ### authomatic color balncing
                    try:
                        output_dir_mosaic = os.path.join(os.path.dirname(folder), OUTPUT_FOLDER)
                        if not os.path.isdir(output_dir_mosaic):                           
                            os.makedirs(output_dir_mosaic)
                        utils.mosaic_images(folder, output_dir_mosaic, new_file_name_mosprep,  new_file_name_mosdef, NORMALIZE, BALSPEC, CUTMTHD, SORTMTHD, NO_VALUE, PIX_PATTERN)
                    except PCIException, e:
                        print e
                    except Exception, e:
                        print
                        
    elif DECISION7 == "NO":
        pass
                        
        print("-" * 80)
        print(" Work is finished")
        print("-" * 80)


if __name__ == '__main__':
    main()    




















