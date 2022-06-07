import os                                   
import fnmatch
import shutil  



# --- define constants and global variables
all_input_paths = []

# --- set working directory
working_dir = raw_input("Please state your input folder path: ")

# --- delete files or folders
TO_DELETE_PATTERN = raw_input("Please give pattern to delete which located on the end of the filename "" _TO_DELETE_PATTERN.file_format"": ")


print("")
print("2. Clean up unnecessary files and directories... ")
print("")     


# --- find file in folder with defined pattern 
for folders in os.listdir(working_dir):
        all_input_paths.append(os.path.join(working_dir, folders))

# --- delete file
for in_folder in all_input_paths:
        in_file  = os.listdir(in_folder)
        for in_file in fnmatch.filter(in_file, ('*' + TO_DELETE_PATTERN)):
                print "file %s was found" %  os.path.join(in_folder, in_file)
                if os.path.exists(os.path.join(in_folder, in_file)):
                        os.remove(os.path.join(in_folder, in_file))
                else:
                        print(in_file + ' file does not exist')



print("")
print(" Clean up is finished... ")
print("")

               
    



