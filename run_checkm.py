#run checkm, checkm should be accessible and database should be ready
def run_checkm(output_folder, input_folder, threads=1, db_path="/home/xiaofang/Documents/checkm_data_2015_01_16"):
    import os
    import subprocess

    # Create full path for output folder in home directory
    home_dir = os.path.expanduser("~")
    output_path = os.path.join(home_dir, output_folder)

    # Create output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)

    try:
        # First set the CheckM data root
        set_root_cmd = [
            "/home/xiaofang/anaconda3/bin/checkm", 
            "data", 
            "setRoot",
            db_path
        ]
        subprocess.run(set_root_cmd, check=True)
        print(f"Successfully set CheckM data root to {db_path}")

        # Then run the main CheckM analysis
        checkm_cmd = [
            "/home/xiaofang/anaconda3/bin/checkm",
            "lineage_wf",
            "-t", str(threads),  # Add threads parameter
            input_folder,
            output_path
        ]
        subprocess.run(checkm_cmd, check=True)
        print(f"Successfully ran CheckM analysis from {input_folder} to {output_path} using {threads} threads")
    except subprocess.CalledProcessError as e:
        print(f"Error running CheckM command")
        print(e)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
