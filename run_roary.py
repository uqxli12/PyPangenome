import os
import subprocess
import getpass

def run_roary(roary_path, output_folder_name, num_clusters, similarity_threshold, num_threads, input_files_path):
    # Create the output folder in the home directory
    home_dir = os.path.expanduser('~')
    output_folder_path = os.path.join(home_dir, output_folder_name)
    
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)
    
    # Prompt the user for their sudo password
    sudo_password = getpass.getpass(prompt='Enter your sudo password: ')
    
    # Construct the Roary command
    command = f"echo {sudo_password} | sudo -S {roary_path} -f {output_folder_path} -e -g {num_clusters} -i {similarity_threshold} -p {num_threads} {input_files_path}"
    
    try:
        # Run the Roary command
        subprocess.run(command, shell=True, check=True)
        print(f"Successfully ran Roary with command: {command}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to run Roary: {e}")