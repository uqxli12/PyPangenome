def run_antismash_batch(folder_path, antismash_outfolder, antismash_path="/home/xiaofang/anaconda3/envs/antismash_bacLIFE/bin/antismash"):
    # Create parent directory in home folder
    import os
    import re
    import subprocess
    home_dir = os.path.expanduser("~")
    parent_dir = os.path.join(home_dir, antismash_outfolder)
    os.makedirs(parent_dir, exist_ok=True)

    # Create antismash output directory inside parent directory
    antismash_dir = os.path.join(parent_dir, "antismash")
    if not os.path.exists(antismash_dir):
        os.makedirs(antismash_dir)

    # Define patterns for matching
    output_dir_pattern = '{genus}_{species}_{strain}'
    file_name_pattern = r'^([^_]+)_([^_]+)_(.+?)\.gbk$'  # Fixed pattern for .gbk files
    folder_name_pattern = r'^([^_]+)_([^_]+)_(.+?)$'     # Fixed pattern for folder names

    # Change to prokka folder
    os.chdir(folder_path)

    # Process each folder
    for folder_name in os.listdir(folder_path):
        if os.path.isdir(folder_name):
            print(f"Processing folder: {folder_name}")

            if re.match(folder_name_pattern, folder_name):
                os.chdir(folder_name)
                print(f'Current directory: {os.getcwd()}')

                # Look for gbk files
                for input_file in os.listdir('.'):
                    if input_file.endswith('.gbk'):
                        print(f"Processing file: {input_file}")

                        match = re.match(file_name_pattern, input_file)
                        if match:
                            print(f"Running antismash for: {input_file}")
                            genus, species, strain = match.groups()
                            print(f"Genus: {genus}, Species: {species}, Strain: {strain}")

                            # Create output directory inside antismash directory
                            output_dir = output_dir_pattern.format(
                                genus=genus,
                                species=species,
                                strain=strain
                            )
                            output_dir = os.path.join(antismash_dir, output_dir)
                            print(f'Creating directory: {output_dir}')
                            os.makedirs(output_dir, exist_ok=True)

                            # Run antismash
                            input_path = os.path.join(folder_path, folder_name, input_file)
                            try:
                                antismash_cmd = (
                                    f"{antismash_path} "
                                    f"--cb-general --cb-knownclusters --cb-subclusters "
                                    f"--output-dir {output_dir} "
                                    f"--genefinding-tool prodigal "
                                    f"--output-basename {genus}_{species}_{strain} "
                                    f"--asf --pfam2go --smcog-trees {input_path}"
                                )  #here the --genefinding-tool option is essential in my test
                                subprocess.check_call(antismash_cmd, shell=True)
                                print(f"Antismash completed for {input_file}")
                            except subprocess.CalledProcessError as e:
                                print(f"Error running antismash for {input_file}: {e}")
                        else:
                            print('Filename does not match expected pattern')

                # Change back to parent directory before next iteration
                os.chdir(folder_path)
            else:
                print('Folder name does not match expected pattern')

    print("Antismash batch processing completed.")