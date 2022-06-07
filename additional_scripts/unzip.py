import tarfile
import os
import utils
import shutil


# --- Definition of constants and functions

TAR = "tar"
GZ = "gz"
ZIP = "zip"

def unzip_file(fname, new_fname_dir):   
    if not os.path.exists(new_fname_dir):
        if (fname.endswith(TAR + "." + GZ)):
            tar = tarfile.open(fname, "r:" + GZ)
            tar.extractall(new_fname_dir)
            tar.close()
            print("." + TAR + "." + GZ + " was unzip")
        elif (fname.endswith(TAR)):
            tar = tarfile.open(fname, "r:")
            tar.extractall(new_fname_dir)
            tar.close()
            print("." + ZIP + "was unzip")
    else: print('file   ' + fname  + '   already exist')




# --- create output directory
print(" 1. setting the working directory...")
print("")
    
working_directory = raw_input("Please state your input folder path: ")
new_output_directory = raw_input("Please give the name of the new directory to store unzip files: ")

            
# --- unzip files
for fn in os.listdir(working_directory):
    fname = os.path.join(working_directory, fn)
    new_fname_dir = os.path.join(os.path.dirname(working_directory), new_output_directory, fn.split('.', 2)[0].split('-', 1)[0])
    unzip_file(fname, new_fname_dir)


print("")
print(" Work is finished... ")
print("")

               
    



