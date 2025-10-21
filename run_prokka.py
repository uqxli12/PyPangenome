def run_prokka_batch(prokka_outfolder, folder_path='/home/xiaofang/genome_renamed', prokka_path='/home/xiaofang/anaconda3/bin/prokka'):
    """
    Run Prokka annotation on multiple genome files in a directory.
    Each genome filename should follow the pattern: genus_species_strain.fna
    Output directories will be created under a parent folder in the user's home directory.
    
    Args:
        parent_folder_name: Name of the parent folder to create in home directory
        folder_path: Path to directory containing input genome files
        prokka_path: Path to the Prokka executable
    """
    import os
    import re
    import subprocess

    # Get home directory and create parent folder
    home_dir = os.path.expanduser("~")
    parent_dir = os.path.join(home_dir, prokka_outfolder)
    os.makedirs(parent_dir, exist_ok=True)

    # Define regex pattern for extracting genome info
    pattern = r'^([^_]+)_([^_]+)_(.+?)\.fna$'

    # Process each file in the folder
    for filename in os.listdir(folder_path):
        if re.match(pattern, filename):
            # Extract genome components from filename
            match = re.match(pattern, filename)
            genus, species, strain = match.groups()

            # Create output directory in parent folder
            output_dir = f'{genus}_{species}_{strain}'
            output_dir_path = os.path.join(parent_dir, output_dir)
            os.makedirs(output_dir_path, exist_ok=True)

            # Build and run Prokka command
            try:
                prokka_cmd = [
                    prokka_path,
                    "--force",
                    "--outdir", output_dir_path,
                    "--prefix", f"{genus}_{species}_{strain}",
                    "--locustag", strain,
                    "--addgenes",
                    "--increment", "5",
                    "--centre", "NIOO-KNAW",
                    "--genus", genus,
                    "--species", species,
                    "--strain", strain,
                    "--evalue", "1e-03",
                    "--rfam",
                    os.path.join(folder_path, filename)
                ]
                subprocess.run(prokka_cmd, check=True)
                print(f"Prokka completed for {filename}")
            except subprocess.CalledProcessError as e:
                print(f"Error running Prokka for {filename}: {e}")
        else:
            print(f'Filename not matching expected pattern: {filename}')

    print("Prokka batch processing completed.")