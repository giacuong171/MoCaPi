#!/usr/bin/env python

## Import packages
import pandas as pd
import argparse


def get_output_files(df):
    filtered_df = df[df["is_noise"] != True]
    cellxgene_table=filtered_df.groupby(["cell","gene"]).size().reset_index()
    cellxgene_df = cellxgene_table.pivot(index='gene', columns='cell', values=0).fillna(0).astype(int)
    cellxgene_df = cellxgene_df.reset_index()
    polygon_df = filtered_df[['x','y','cell']]
    polygon_df['x']= polygon_df['x'].astype(int)
    polygon_df['y']= polygon_df['y'].astype(int)
    return cellxgene_df,polygon_df

if __name__ == "__main__":
    # Add a python argument parser with options for input, output and image size in x and y
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--baysor_segmentation", help="Spot table to project.")
    # parser.add_argument("--config_baysor",help="Config of baysor")
    parser.add_argument(
        "--output_cellxgene",
        type=str,
        help="Output path of spot table file with column name, which is needed for baysor",
    )
    parser.add_argument(
        "--output_polygon",
        type=str,
        help="Output path of gene ratio table, which contains information about nucleus expressed genes and cytoplasmic expressed gene",
    )
    parser.add_argument("--version", action="version", version="0.1.0")

    args = parser.parse_args()

    baysor_df = pd.read_csv(args.baysor_segmentation,header=0,sep=",")
    cellxgene_df,polygon_df = get_output_files(baysor_df)
    cellxgene_df.to_csv(args.output_cellxgene,index=False,header=True,sep=",")
    polygon_df.to_csv(args.output_polygon,index=False,header=True,sep=",")