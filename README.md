# Molecular_Cartography_Segmentation_pipeline
Molecular Cartography segmentation pipeline is a cell segmentation pipeline tool for molecular cartography images from the company Resolved Bioscience. 

# Outline
-------
- [Molecular\_Cartography\_Segmentation\_pipeline](#molecular_cartography_segmentation_pipeline)
- [Outline](#outline)
- [Concept](#concept)
- [Quick-Start](#quick-start)
  - [Installation via Conda/Mamba](#installation-via-condamamba)
  - [Configuration](#configuration)
  - [Running the pipeline](#running-the-pipeline)

# Concept
-------
Molecular cartography segmentation pipeline is created with the purpose to help scientist to be able to do cell segmentation on the molecular cartography images without having much knowledge in this field.

# Quick-Start
-------

## Installation via Conda/Mamba

After cloning this git repository:
```
https://gitlab.cubi.bihealth.org/phgi10/molecular_cartography_segmentation_pipeline.git
```

First, you need to install snakemake with Conda/Mamba. Please follow this [link](https://snakemake.readthedocs.io/en/stable/getting_started/installation.html) to have more information. 

## Configuration

  1. Create a samplesheet.csv file. The file should follow below format:
```
sample,nuclear_image,spot_table
A,path/to/DAPI/images_A.tif,path/to/spot/table/A.spot_table.txt
B,path/to/DAPI/images_B.tif,path/to/spot/table/B.spot_table.txt
```

   2. Config the pipeline and parameters. \
There are three parameters that you need to change in the config.yaml file:\
    - samples is path to your samplesheet.csv file \
    - result_dir is path where you want to store your output \
    - models_path is the directory to the pretrained model of cellpose, which you need to download from [cellpose](https://cellpose.readthedocs.io/en/latest/models.html) or from this [link](https://drive.google.com/file/d/1zHGFYCqRCTwTPwgEUMNZu0EhQy2zaovg/view)

## Running the pipeline
Activate the conda environment, which contains snakemake and run the following command.
```
snakemake --cores all --use-conda
```