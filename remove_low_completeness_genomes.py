import os
import shutil
import ast
from pathlib import Path

# File paths (ADJUST THESE IF NEEDED)
stats_file = "/home/xiaofang/wheat_endophyte_genomes_checkm/storage/bin_stats_ext.tsv"
genome_dir = "/home/xiaofang/wheat_endophyte_genomes_renamed"
new_dir = str(Path.home() / "low_completeness_genomes")  # Home directory output
file_extension = ".fna"

# Create output directory
os.makedirs(new_dir, exist_ok=True)

# Initialize counters
kept_count = 0
removed_count = 0

# Process CheckM stats
with open(stats_file, 'r') as f:
    for line in f:
        parts = line.strip().split('\t')
        if len(parts) < 2:
            continue
            
        species_name = parts[0]
        data_str = parts[1]
        
        try:
            data_dict = ast.literal_eval(data_str)
            completeness = data_dict.get('Completeness')
            
            if completeness is None:
                print(f"Warning: 'Completeness' missing for {species_name}")
                continue
                
            # Handle completeness values
            if completeness >= 97.0:
                kept_count += 1
            else:
                removed_count += 1
                print(f"{species_name}: Completeness = {completeness}% (moving to {new_dir}/)")
                
                genome_file = os.path.join(genome_dir, species_name + file_extension)
                
                if os.path.exists(genome_file):
                    shutil.move(
                        genome_file, 
                        os.path.join(new_dir, os.path.basename(genome_file))
                    )
                else:
                    print(f"  Error: Genome file not found - {genome_file}")
                    
        except Exception as e:
            print(f"Error processing {species_name}: {str(e)}")

# Print summary report
print("\n" + "="*50)
print(f"GENOME PROCESSING SUMMARY:")
print(f"• High-completeness genomes kept (≥97%): {kept_count}")
print(f"• Low-completeness genomes moved (<97%): {removed_count}")
print("="*50)
print("Operation complete.")
