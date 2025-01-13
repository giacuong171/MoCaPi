import pandas as pd
import argparse

# def get_nucleus_cyto(ratio_files):
#     numb_files = len(ratio_files)
#     all_ratio_df=pd.DataFrame()
#     for file in ratio_files:
#         ratio_df = pd.read_csv(file,header=0)
#         ratio_df = ratio_df.set_index('genes')
#         all_ratio_df = all_ratio_df.add(ratio_df,fill_value=0)
#     all_ratio_df["ratio"] = all_ratio_df["ratio"]/numb_files
#     return all_ratio_df

if __name__ == "__main__":
    # Add a python argument parser with options for input, output and image size in x and y
    parser = argparse.ArgumentParser()
    parser.add_argument('--ratio_file',help='file contains ratio')
    parser.add_argument("-x",default='x',help="column name in spot table")
    parser.add_argument("-y",default='y',help="column name in spot table")
    parser.add_argument("-z",default='z',help="column name in spot table")
    parser.add_argument("-gene",default='gene',help="column name in spot table")
    parser.add_argument("--force_2d",default=True,help="Ignores z-column in the data if it is provided")
    parser.add_argument("--min_molecules_per_gene",default=1,help=" Minimal number of molecules per gene")
    parser.add_argument("--exclude_genes",default='',help="Comma-separated list of genes or regular expressions to ignore during segmentation. Example: 'Blank*,MALAT1'")
    parser.add_argument("--min_molecules_per_cell",default=3,help=" Minimal number of molecules for a cell to be considered as real. It's an important parameter, as it's used to infer several other parameters")
    parser.add_argument("--min_molecules_per_segment",default=2,help="Minimal number of molecules in a segmented region, required for this region to be considered as a possible cell. Default: min-molecules-per-cell / 4")
    parser.add_argument("--confidence_nn_id",default=3,help="Number of nearest neighbors to use for confidence estimation. Default: min-molecules-per-cell / 2 + 1")
    parser.add_argument("--scale",default=-1.0,help="Negative values mean it must be estimated from `min_molecules_per_cell`")
    parser.add_argument("--scale_std",default="25%",help="Standard deviation of scale across cells. Can be either number, which means absolute value of the std, or string ended with '%' to set it relative to scale. Default: '25%'")
    parser.add_argument("--estimate_scale_from_centers",default=True,help="column name in spot table")
    parser.add_argument("--n_clusters",default=1,help="column name in spot table")
    parser.add_argument("--prior_segmentation_confidence",default=0.9,help="column name in spot table")
    parser.add_argument("--iters",default=500,help="column name in spot table")
    parser.add_argument("--n_cells_init",default=0,help="column name in spot table")
    parser.add_argument("--nuclei_genes",default='',help="column name in spot table")
    parser.add_argument("--cyto_genes",default='',help="column name in spot table")
    parser.add_argument("--new_component_weight",default=0.2,help="column name in spot table")
    parser.add_argument("--new_component_fraction",default=0.3,help="column name in spot table")
    parser.add_argument("--gene_composition_neigborhood",default=0,help="column name in spot table")
    parser.add_argument("--min_pixels_per_cell",default=15,help="column name in spot table")
    
    parser.add_argument(
        "--config_toml", type=str, help="Output path of config file"
    )
    parser.add_argument("--version", action="version", version="0.1.0")

    args = parser.parse_args()
    force_2d='true' if args.force_2d else 'false'
    # if int(args.min_molecules_per_segment) * 4 != int(args.min_molecules_per_cell): 
    #     raise ValueError("min_molecules_per_segment = min-molecules-per-cell / 4")
    
    # if (int(args.confidence_nn_id) - 1 ) * 2 != int(args.min_molecules_per_cell):
    #     raise ValueError("min_molecules_per_segment = min-molecules-per-cell / 2 + 1")

    estimate_scale_from_centers = "true" if args.estimate_scale_from_centers else "false"
    ratio_df = pd.read_csv(args.ratio_file,sep=',',header=0)
    nuclei_list = ratio_df[ratio_df['Ratio'] >= 0.7].gene.tolist()
    cyto_list = ratio_df[ratio_df['Ratio'] <= 0.3].gene.tolist()
    nuclei_genes = ",".join(nuclei_list)
    cyto_genes = ",".join(cyto_list)
    config_content = f"""
# Config file for baysor
[data]
x = "{args.x}" # Name of the x column in the input data. Default: "x"
y = "{args.y}" # Name of the y column in the input data. Default: "y"
z = "{args.z}" # Name of the y column in the input data. Default: "z"
gene = "{args.gene}" # Name of gene column in the input data. Default: "gene"
force_2d = {force_2d} # Ignores z-column in the data if it is provided
min_molecules_per_gene = {args.min_molecules_per_gene}  # Minimal number of molecules per gene. Default: 1
exclude_genes = "{args.exclude_genes}" # Comma-separated list of genes or regular expressions to ignore during segmentation. Example: 'Blank*,MALAT1'
min_molecules_per_cell = {int(args.min_molecules_per_cell)} # Minimal number of molecules for a cell to be considered as real. It's an important parameter, as it's used to infer several other parameters. Default: 3
min_molecules_per_segment = {int(args.min_molecules_per_segment)} # Minimal number of molecules in a segmented region, required for this region to be considered as a possible cell. Default: min-molecules-per-cell / 4
confidence_nn_id = {int(args.confidence_nn_id)} # Number of nearest neighbors to use for confidence estimation. Default: min-molecules-per-cell / 2 + 1

[segmentation]
scale = {args.scale} # Negative values mean it must be estimated from `min_molecules_per_cell`
scale_std = "{args.scale_std}" # Standard deviation of scale across cells. Can be either number, which means absolute value of the std, or string ended with "%" to set it relative to scale. Default: "25%"
estimate_scale_from_centers = {estimate_scale_from_centers} # Use scale estimate from DAPI if provided. Default: true

n_clusters = {int(args.n_clusters)} # Number of clusters to use for cell type segmentation. Default: 4
prior_segmentation_confidence = {args.prior_segmentation_confidence} # Confidence of the prior segmentation. Default: 0.2
iters = {int(args.iters)} # Number of iterations for the cell segmentation algorithm. Default: 500
n_cells_init = {int(args.n_cells_init)} # Initial number of cells

nuclei_genes = "{nuclei_genes}" # Comma-separated list of nuclei-specific genes. If provided, `cyto-genes` has to be set, as well.
cyto_genes = "{cyto_genes}" # Comma-separated list of cytoplasm-specific genes. If provided, `nuclei-genes` has to be set, as well.

# The parameters below are not supposed to be changed normally
new_component_weight = {args.new_component_weight} # Prior weight of assignment a molecule to new component. Default: 0.2
new_component_fraction = {args.new_component_fraction} # Fraction of distributions, sampled at each stage. Default: 0.3

[plotting]
gene_composition_neigborhood = {int(args.gene_composition_neigborhood)} # Number of neighbors (i.e. 'k' in k-NN), which is used for gene composition visualization. Larger numbers leads to more global patterns. Default: estimate from min-molecules-per-cell
min_pixels_per_cell = {int(args.min_pixels_per_cell)} # Number of pixels per cell of minimal size, used to estimate size of the final plot. For most protocols values around 7-30 give enough visualization quality. Default: 15
"""
    with open(args.config_toml, "w") as file:
        file.write(config_content)