#copy all extracted fna files to a new filefolder
def copy_fna_files(target_dir, source_dir):
    """
    Create a directory named target_dir in home folder and copy all .fna files 
    from source_dir and its subdirectories into target_dir
    
    Args:
        target_dir (str): Name of target directory to create
        source_dir (str): Name of source directory to search for .fna files
    """
    import os
    import shutil
    from pathlib import Path

    # Create target directory in home folder
    home_dir = str(Path.home())
    target_path = os.path.join(home_dir, target_dir)
    os.makedirs(target_path, exist_ok=True)

    # Walk through source directory and find .fna files
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.fna'):
                source_file = os.path.join(root, file)
                # Copy file to target directory
                shutil.copy2(source_file, target_path)