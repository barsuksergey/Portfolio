import os

curr_dir = os.getcwd()
new_dir = os.path.join(curr_dir,"All files")

if not os.path.isdir(new_dir):
    os.mkdir(new_dir)

os.chdir("All files")
destination = os.getcwd()

os.chdir('..')
os.chdir('inbox')

counter = 1
folders = os.listdir()

# Instagram messages are kept in folder "inbox" and are json files, this moves them all into "All files" dir
# counter is needed to avoid re-writing files as they are all named "messages"
for folder in folders:
    os.chdir(folder)
    files = os.listdir()
    for file in files:
        if ".json" in os.path.basename(file):
            file_path = os.path.abspath(file)
            file_name = f"{counter}" + "-" + os.path.basename(file)
            counter += 1
            os.rename(file_path, os.path.join(destination,file_name))
    os.chdir('..')
