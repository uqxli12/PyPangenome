import os
import subprocess

def batch_download_genomes(file_path, output_folder):
    # Create and change to the output directory
    home_dir = os.path.expanduser('~')
    new_folder_path = os.path.join(home_dir, output_folder)
    
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
    
    os.chdir(new_folder_path)
    print(f"Current working directory: {os.getcwd()}")

    # Read accession numbers from the file
    with open(file_path, 'r') as file:
        accession_numbers = file.read().splitlines()
    
    # Download genomes for each accession number
    for accession_number in accession_numbers:
        command = f'datasets download genome accession {accession_number}'
        try:
            # Execute the datasets command
            subprocess.run(command, shell=True, check=True)
            print(f'Successfully downloaded genome for {accession_number}')
            if os.path.exists("ncbi_dataset.zip"):
                os.rename("ncbi_dataset.zip", f"{accession_number}.zip")
        except subprocess.CalledProcessError as e:
            print(f'Failed to download genome for {accession_number}: {e}')