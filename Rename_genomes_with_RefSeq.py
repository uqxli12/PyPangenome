#extract the RefSeq number from the fna files, compare it with the metadata file, rename it with its strain name
def process_files(target_folder, source_folder, excel_file):
    import os
    import shutil
    import pandas as pd
    from pathlib import Path

    # Create target folder in home directory
    home = str(Path.home())
    target_path = os.path.join(home, target_folder)
    os.makedirs(target_path, exist_ok=True)

    # Read excel file
    df = pd.read_excel(excel_file)
    
    # Get list of files from source folder
    for filename in os.listdir(source_folder):
        try:
            # Extract part before second underscore
            parts = filename.split('_')
            if len(parts) >= 2:
                ref_id = '_'.join(parts[:2])
                
                # Find matching RefSeq in excel
                match = df[df['RefSeq'] == ref_id]
                if not match.empty:
                    # Get corresponding strain name
                    strain_name = match.iloc[0]['Strain']
                    
                    # Get file extension
                    _, ext = os.path.splitext(filename)
                    
                    # Copy and rename file
                    source_file = os.path.join(source_folder, filename)
                    target_file = os.path.join(target_path, f"{strain_name}{ext}")
                    shutil.copy2(source_file, target_file)
                    
        except Exception as e:
            print(f"Error processing file {filename}: {str(e)}")