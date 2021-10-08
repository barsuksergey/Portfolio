import os
import sys


formats = sys.argv[2:]
folder = sys.argv[1]

curr_dir = os.getcwd()
new_dir = os.path.join(curr_dir,f"{folder}_all_files")

if not os.path.isdir(new_dir):
    os.mkdir(new_dir)

os.chdir(f"{folder}_all_files")
destination = os.getcwd()
os.chdir('..')

def dig_dir(folder, *args):
    args = formats
    os.chdir(folder)
    dirs = os.listdir()
    for dir in dirs:
        if any([x in dir for x in args]):
            file_path = os.path.abspath(dir)
            file_name = os.path.basename(dir)
            os.rename(file_path, os.path.join(destination,file_name))
        else:
            dig_dir(dir)
    os.chdir('..')

    
if __name__ == '__main__':
    dig_dir(folder, formats)
