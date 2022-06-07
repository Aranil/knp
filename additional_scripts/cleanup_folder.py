import os                                   
import fnmatch
import shutil  



# --- define constants and global variables
all_input_paths = []

# --- set working directory
working_dir = raw_input("Please state your input folder path: ")

# --- delete files or folders
FOLDER_NAME = raw_input("Please give the name of folder to delete: ")

print("")
print("2. Clean up unnecessary files and directories... ")
print("")     


# --- find file in folder with defined pattern 
for folders in os.listdir(working_dir):
        all_input_paths.append(os.path.join(working_dir, folders))

# --- delete file
for in_file in all_input_paths:
    if os.path.exists(os.path.join(in_file, FOLDER_NAME)):
        print('file exist and will be removed:   ' + os.path.join(in_file, FOLDER_NAME))
        shutil.rmtree(os.path.join(in_file, FOLDER_NAME))
    else:
        print('file not exist')


print("")
print(" Clean up is finished... ")
print("")

               
    



