import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

class PlotGenerator:
    def __init__(self):
        pass
    
    def boxplot_plot(self, input_file, output_path, style):
        mydata = pd.read_csv(input_file, sep='\\t', header=None, converters={i: float for i in range(23)})
        fig, ax = plt.subplots(figsize=(6, 4))
        
        if style == 'cell':
            ax.set_facecolor('lightgrey')
            ax.grid(True, color='white', linestyle='-', linewidth=0.5)
        elif style == 'nature':
            ax.set_facecolor('white')
            ax.grid(True, color='lightgrey', linestyle='--', linewidth=0.5)
        
        ax.boxplot(mydata.values, vert=True, patch_artist=True)
        ax.set_title('Number of new genes')
        ax.set_xlabel('No. of genomes')
        ax.set_ylabel('No. of genes')
        ax.set_ylim(bottom=0)
        #ax.outline_patch.set_edgecolor('black') #如果此处报错，运行&ldquo;pip install --upgrade matplotlib&rdquo;
        
        plt.savefig(output_path, bbox_inches='tight', dpi=300)
        plt.close(fig)
    
    def plot_blast_identity(self, input_file, output_path, style):
        mydata = pd.read_csv(input_file, sep='\\t', header=None, converters={i: float for i in range(23)})
        fig, ax = plt.subplots(figsize=(6, 4))
        
        if style == 'cell':
            ax.set_facecolor('lightgrey')
            ax.grid(True, color='white', linestyle='-', linewidth=0.5)
        elif style == 'nature':
            ax.set_facecolor('white')
            ax.grid(True, color='lightgrey', linestyle='--', linewidth=0.5)
        
        ax.plot(mydata.values, label='Blast percentage identity')
        ax.set_title('Number of blastp hits with different percentage identity')
        ax.set_xlabel('Blast percentage identity')
        ax.set_ylabel('No. blast results')
        
        plt.savefig(output_path, bbox_inches='tight', dpi=300)
        plt.close(fig)
    
    def line_plot_conserved_vs_total(self, input_files, output_path, style):
        conserved = pd.read_csv(input_files[0], sep='\\t', header=None, converters={i: float for i in range(23)}).mean(axis=1)
        total = pd.read_csv(input_files[1], sep='\\t', header=None, converters={i: float for i in range(23)}).mean(axis=1)
        
        genes = pd.DataFrame({
            'genes_to_genomes': pd.concat([conserved, total], axis=0),
            'genomes': list(range(1, len(conserved)+1)) * 2,
            'Key': ['Conserved genes'] * len(conserved) + ['Total genes'] * len(total)
        })
        
        fig, ax = plt.subplots(figsize=(6, 4))
        
        if style == 'cell':
            ax.set_facecolor('lightgrey')
            ax.grid(True, color='white', linestyle='-', linewidth=0.5)
        elif style == 'nature':
            ax.set_facecolor('white')
            ax.grid(True, color='lightgrey', linestyle='--', linewidth=0.5)
        
        ax.plot(genes[genes['Key'] == 'Conserved genes']['genomes'], 
                genes[genes['Key'] == 'Conserved genes']['genes_to_genomes'], 
                label='Conserved genes')
        ax.plot(genes[genes['Key'] == 'Total genes']['genomes'], 
                genes[genes['Key'] == 'Total genes']['genes_to_genomes'], 
                label='Total genes')
        
        ax.set_title('Conserved vs Total Genes')
        ax.set_xlabel('No. of genomes')
        ax.set_ylabel('No. of genes')
        ax.set_xlim(1, len(total))
        ax.set_ylim(1, max(total))
        
        plt.legend(loc='upper left')
        plt.savefig(output_path, bbox_inches='tight', dpi=300)
        plt.close(fig)
    
    def line_plot_unique_vs_new(self, input_files, output_path, style):
        unique_genes = pd.read_csv(input_files[0], sep='\\t', header=None, converters={i: float for i in range(23)}).mean(axis=1)
        new_genes = pd.read_csv(input_files[1], sep='\\t', header=None, converters={i: float for i in range(23)}).mean(axis=1)
        
        genes = pd.DataFrame({
            'genes_to_genomes': pd.concat([unique_genes, new_genes], axis=0),
            'genomes': list(range(1, len(unique_genes)+1)) * 2,
            'Key': ['Unique genes'] * len(unique_genes) + ['New genes'] * len(new_genes)
        })
        
        fig, ax = plt.subplots(figsize=(6, 4))
        
        if style == 'cell':
            ax.set_facecolor('lightgrey')
            ax.grid(True, color='white', linestyle='-', linewidth=0.5)
        elif style == 'nature':
            ax.set_facecolor('white')
            ax.grid(True, color='lightgrey', linestyle='--', linewidth=0.5)
        
        ax.plot(genes[genes['Key'] == 'Unique genes']['genomes'], 
                genes[genes['Key'] == 'Unique genes']['genes_to_genomes'], 
                label='Unique genes')
        ax.plot(genes[genes['Key'] == 'New genes']['genomes'], 
                genes[genes['Key'] == 'New genes']['genes_to_genomes'], 
                label='New genes')
        
        ax.set_title('Unique vs New Genes')
        ax.set_xlabel('No. of genomes')
        ax.set_ylabel('No. of genes')
        ax.set_xlim(1, len(unique_genes))
        ax.set_ylim(1, max(unique_genes))
        
        plt.legend(loc='upper left')
        plt.savefig(output_path, bbox_inches='tight', dpi=300)
        plt.close(fig)
# 调用方法
# 创建实例
#plotter = PlotGenerator()

# 调用方法生成图表 (remember to add the correct paths to your file and saving folder)
#plotter.boxplot_plot("number_of_new_genes.Rtab", "output/number_new_genes.png", "cell")
#plotter.boxplot_plot("number_of_conserved_genes.Rtab", "output/number_of_conserved_genes.png", "nature")
#plotter.boxplot_plot("number_of_genes_in_pan_genome.Rtab", "output/number_of_genes_in_pan.png", "cell")
#plotter.boxplot_plot("number_of_unique_genes.Rtab", "output/number_of_unique_genes.png", "nature")

#plotter.plot_blast_identity("blast_identity_frequency.Rtab", "output/blast_identify_frequency.png", "cell")

#plotter.line_plot_conserved_vs_total(["number_of_conserved_genes.Rtab", "number_of_genes_in_pan_genome.Rtab"], "output/conserved_vs_total_genes.png", "nature")

#plotter.line_plot_unique_vs_new(["number_of_unique_genes.Rtab", "number_of_new_genes.Rtab"], "output/unique_vs_new_genes.png", "cell")
