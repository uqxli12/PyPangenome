#roary takes gff files as inputs for pangenome analysis. Here we collect all gff from prokka annotation to a new folder
import os
import shutil

def copy_gff_files_to_new_folder(new_folder_name, source_folder_name):
    # Create a new folder in the home directory with the name of parameter 1
    home_dir = os.path.expanduser('~')
    new_folder_path = os.path.join(home_dir, new_folder_name)
    
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
    
    # Traverse the folder with the name of parameter 2
    for root, dirs, files in os.walk(source_folder_name):
        for file in files:
            if file.endswith('.gff'):
                # Copy all the found .gff files to the folder named by parameter 1
                source_file_path = os.path.join(root, file)
                destination_file_path = os.path.join(new_folder_path, file)
                shutil.copy2(source_file_path, destination_file_path)
                print(f"Copied {source_file_path} to {destination_file_path}")
