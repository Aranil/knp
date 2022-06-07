import os                                   
import fnmatch
import shutil
import re



# --- define constants and global variables
all_input_paths = {}
folder1_list = []
folder2_list = []

# --- set working directory
working_dir1 = raw_input("Please state your input folder path where is file to move: ")
working_dir2 = raw_input("Please state your input folder path where file should be moved: ")

print("")
print("2. To find file and move it to directory with the same name... ")
print("")     


# --- find file in folder with defined pattern 
for folders1 in os.listdir(working_dir1):
        folder1_list.append(os.path.join(working_dir1, folders1))        
for folders2 in os.listdir(working_dir2):
        folder2_list.append(os.path.join(working_dir2, folders2))        
all_input_paths = dict(zip(folder1_list, folder2_list))

         

for folders1, folders2 in all_input_paths.items():
        for in_file1 in os.listdir(folders1):
                pattern1 = in_file1.split('.', 1)[0].rsplit('_', 3)[0].rsplit('_', 1)[1]
                pattern1 = re.compile(pattern1)
                folder_name2 = os.path.basename(folders2)
                if pattern1.search(folder_name2):
                        if not os.path.exists(os.path.join(folders2, in_file1)):
                                shutil.move(os.path.join(folders1, in_file1), folders2)

       


print("")
print(" Work is finished... ")
print("")

               
    



