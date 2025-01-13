#!/usr/bin/env python

## Import packages
import pandas as pd
import tifffile as tiff
import argparse


def assign_cell2spot(spot_table,cell_mask):
    # Exclude any rows that contain Duplicated in the gene column from spot_table
    spot_table = spot_table[~spot_table["gene"].str.contains("Duplicated")]
    cell=[]
    # Iterate over each row in the grouped DataFrame
    for index, row in spot_table.iterrows():
        # Get the x and y positions and gene
        x = int(row["x"])
        y = int(row["y"])
        # gene = row["gene"]
        cell.append(cell_mask[y,x])
    spot_table.loc[:,'cell'] = cell
    return spot_table


def cyto_nucleus_ratio(spot_table):
    total_spots = spot_table.loc[:, "gene"].value_counts().reset_index()
    no_outliner_genes=spot_table[spot_table['cell'] != 0]
    numb_nucleus = no_outliner_genes.loc[:, "gene"].value_counts().reset_index()
    ratio_df = pd.merge(total_spots, numb_nucleus, on='gene',how='outer')
    ratio_df = ratio_df.rename(columns={'count_x':'totalCounts','count_y':'NucleusCounts'})
    ratio_df['Ratio'] = ratio_df['NucleusCounts']/ratio_df['totalCounts']
    return ratio_df



if __name__ == "__main__":
    # Add a python argument parser with options for input, output and image size in x and y
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--spot_table", help="Spot table to project.")
    parser.add_argument("-c", "--cell_mask", help="Sample ID.")
    # parser.add_argument("--config_baysor",help="Config of baysor")
    parser.add_argument(
        "--output_spot_table",
        type=str,
        help="Output path of spot table file with column name, which is needed for baysor",
    )
    parser.add_argument(
        "--output_ratio",
        type=str,
        help="Output path of gene ratio table, which contains information about nucleus expressed genes and cytoplasmic expressed gene",
    )
    parser.add_argument("--version", action="version", version="0.1.0")

    args = parser.parse_args()

    ## Read in spot table
    spot_data = pd.read_csv(
        args.spot_table,
        names=["x", "y", "z", "gene", "empty"],
        sep="\t",
        header=None,
        index_col=None,
    )

    cell_mask = tiff.imread(args.cell_mask)

    spot_table = assign_cell2spot(spot_data,cell_mask)
    ratio_df = cyto_nucleus_ratio(spot_table)

    spot_table.to_csv(args.output_spot_table, sep=",", header=True, index=False)
    ratio_df.to_csv(args.output_ratio,sep=",",header=True, index=False)