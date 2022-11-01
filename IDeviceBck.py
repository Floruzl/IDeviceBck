# imports probably needed
from win32com.shell import shell, shellcon
from win32com.propsys import propsys
from configparser import ConfigParser
import pythoncom

import sys
import os
#import os.path

import numpy as np
import time

# Recursive function to browse into a non filesystem path
# Thanks to @Stephen Brody and @Lani for this function supplied in https://stackoverflow.com/questions/62909927/
def recurse_and_get_ishellfolder(base_ishellfolder, path):
    splitted_path = path.split("\\", 1)
    #print(splitted_path)
    for pidl in base_ishellfolder:
        if base_ishellfolder.GetDisplayNameOf(pidl, shellcon.SHGDN_NORMAL) == splitted_path[0]:
            break

    folder = base_ishellfolder.BindToObject(pidl, None, shell.IID_IShellFolder)

    if len(splitted_path) > 1:
        # More to recurse
        return recurse_and_get_ishellfolder(folder, splitted_path[1])
    else:
        return folder


# Copy the a singe file from iPhone to PC
# Thanks to @Stephen Brody and @Lani for this function supplied in https://stackoverflow.com/questions/62909927/
def copy_file(src_ishellfolder, src_pidl, dst_ishellfolder, dst_filename):
    fidl = shell.SHGetIDListFromObject(src_ishellfolder)  # Grab the PIDL from the folder object
    didl = shell.SHGetIDListFromObject(dst_ishellfolder)  # Grab the PIDL from the folder object

    si = shell.SHCreateShellItem(fidl, None, src_pidl)  # Create a ShellItem of the source file
    dst = shell.SHCreateItemFromIDList(didl)

    pfo = pythoncom.CoCreateInstance(shell.CLSID_FileOperation, None, pythoncom.CLSCTX_ALL, shell.IID_IFileOperation)
    pfo.SetOperationFlags(shellcon.FOF_NOCONFIRMATION | shellcon.FOF_SILENT | shellcon.FOF_NOERRORUI)
    pfo.CopyItem(si, dst, dst_filename) # Schedule an operation to be performed
    pfo.PerformOperations()
    return not pfo.GetAnyOperationsAborted()




# throw everything in the ishellfolder in a list
def make_file_list(iShellFolder):
    file_list=[]
    for pidl in iShellFolder:
        if(iShellFolder.GetDisplayNameOf(pidl, shellcon.SHGDN_NORMAL)):
             file_list.append(iShellFolder.GetDisplayNameOf(pidl, shellcon.SHGDN_NORMAL))
    return file_list
             
# if there is a skip list in the folder return it else return empty list
def get_skip_list(path):
    path=path+"\\skip_list.npy"
    skip_list=np.array([])
    if (os.path.exists(path)):
        skip_list=np.load(path)
    return skip_list.tolist()

# if there is a skip list in the folder add to it else make one
def add_to_skip_list(path ,file):
    path=path+"\\skip_list.npy"
    skip_list=np.array([])
    
    if (os.path.exists(path)):
        skip_list=np.load(path)
        if not file in skip_list:
            skip_list=np.append(skip_list,file)
    else:
        skip_list=np.array([file])
    np.save(path ,skip_list)
    return skip_list.tolist()
    




# this function runs through all the files in the supplied folder
# and copies them into the destination folder
# Note the source (src) is an iShell object 
# The destination (dst) a regular string path to an (existing) folder

def folder_copy(current_src_shell,current_dst_reg):
    # get a list of files from src folder
    src_file_list=make_file_list(current_src_shell)
    
    # get a list of files from dst folder
    pidl_folder_dst, flags = shell.SHILCreateFromPath(current_dst_reg , 0)
    current_dst_shell = shell.SHGetDesktopFolder().BindToObject(pidl_folder_dst, None, shell.IID_IShellFolder)

    dst_file_list=make_file_list(current_dst_shell)

    nr_src_files= len(src_file_list)
    nr_dest_files=len(dst_file_list)
    
    # remove duplicates (AKA wtf Apple really?) 
    move_list=set(src_file_list.copy())
    nr_min_exp_dst=len(move_list)
    
    # nr of duplicate files (which version of IOS are we on again? ;o)
    nr_duplicate_files=nr_src_files - len(move_list)
    
    # subtract dst_file_list from src_file_list
    for i in dst_file_list:
        if i in move_list:
            move_list.remove(i)
     
    # if there is a skiplist in dst folder get that
    skip_list=get_skip_list(current_dst_reg)
    nr_skip_files=len(skip_list)
    nr_min_exp_dst=nr_min_exp_dst-nr_skip_files
    
   
    # subtract skip_file_list from move_file_list
    for i in skip_list:
        if i in move_list:
            move_list.remove(i)
            
    nr_left_to_move=len(move_list)
    
    print("src: " + str(nr_src_files) +
          " dst: " + str(nr_dest_files) +
          " skip: " + str(nr_skip_files) +  
          " dups: " + str(nr_duplicate_files)   )

    print("left to copy: " + str(nr_left_to_move) +
          " minimum files in dst : " + str(nr_min_exp_dst) )
    
    # MOVE THE ACTUAL LIST

    # if list not empty
    if len(move_list)>0:
        # MOVE_LOOP
        # loop through the source file folder
        for pidl in current_src_shell:
            file_name=current_src_shell.GetDisplayNameOf(pidl, shellcon.SHGDN_NORMAL)
            
            # if current pidl (file) matches a filename in the move_list
            if ( file_name in move_list):
                
                # try move from src_file_list to dst_folder
                if not (copy_file(current_src_shell, pidl, current_dst_shell, file_name)):
                    print("FAILED moving file " + file_name + " adding to skip_list")
                    #   if fail
                    #       add file to skip list
                    add_to_skip_list(current_dst_reg,file_name)
                    #       remove file from MOVE_LIST
                    move_list.remove(file_name)
                    return False

                else:
                    print("Succesfully copied file " + current_dst_reg + "\\" + file_name)
                    move_list.remove(file_name)
    else:
        print("ALREADY DONE!! Skipping yay! "  )
    return True



# PREP
base= shell.SHGetDesktopFolder()

dst_path_reg=''
src_path_ishell=''

# if there is no config.ini make one
if(os.path.isfile('config.ini')):
    #load and read the config file
    config_object = ConfigParser()
    config_object.read("config.ini")
    directories = config_object["Directories"]
    src_path_ishell=directories["IPhone DCIM Directory"]
    dst_path_reg=directories["Destination Directory"]
    
else:
    #create ini file
    print("no config file detected, creating one")

    
    config_object = ConfigParser()
    config_object["Directories"] = {
        "IPhone DCIM Directory": "This PC\\Apple iPhone\\Internal Storage\\DCIM",
        "Destination Directory": "C:\\IPhoneBackup",
    }
    with open('config.ini', 'w') as conf:
        config_object.write(conf)

if not( dst_path_reg == '' or src_path_ishell == '' ):
    print("Preparing to copy from : " + src_path_ishell)
    print("to : " + dst_path_reg)
    input("Press Enter to continue...")
    

else:
    print("Update the source and destination directory in the .ini file and run again")
    input("Press Enter to continue...")
    sys.exit()









# get all the folders from the supplied DCIM folder stick them in a sorted list
try:
    current_src_shell=recurse_and_get_ishellfolder(base,src_path_ishell)
    directories_to_copy=make_file_list(current_src_shell)
    directories_to_copy.sort()
except:
    print("Failed make list of source directories")
    print("Most likely your Iphone source path is incorrect, it is not connected, or not ready")
    print("Always make sure you can open an image in explorer before starting")
    input("Press Enter to continue...")
    sys.exit()
    

# go through all directories, make a new destination dir if necessary and copy the files
for i in directories_to_copy:
    current_src_shell=recurse_and_get_ishellfolder(base , src_path_ishell + "\\" + i)
    src_file_list=make_file_list(current_src_shell)

    
    if(len(src_file_list)>0):
        newpath= dst_path_reg + '\\' + i
        print("-----------------------------------------------" )
        print("STARTING directory " + newpath )
        
        if not os.path.exists(newpath):
            os.makedirs(newpath)

        
        if not (folder_copy(current_src_shell, newpath)):
            print("-----------------------------------------------" )
            print("Copying failed most likely because corrupt file")
            print("This often causes your iphone to become unavailable/unresponsive")
            print("test by opening an image file from you phone in explorer ")
            print("if you cannot, unplug and plug back in, or just restart iphone")
            print("")
            print("once you can open an image from your phone in explorer")
            print("re run this program to continue where you left off")
            print("the corrupt file will be skipped")
            print("")
            print("DO NOT restart the program unless you can open an image form your phone in explorer")
            print("otherwise it will keep adding files to the skip_list. you can delete")
            print("the skiplist eg: " + newpath + "\\skip_file.npy and re run to retry the files")
            print("")            
            input("Press Enter to continue...")
            sys.exit()
            break
        else:
            print("DONE copying files to directory " + newpath )
    else:
        print("SKIPPING empty directory")

print("DONE")
input("Press Enter to continue...")   
    
