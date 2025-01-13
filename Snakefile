import pandas as pd
import os
configfile: "config.yaml"

include: "rules/mindagap/mindagap.smk"
include: "rules/cellpose/cellpose.smk"
include: "rules/baysor/preprocess/preprocessing.smk"
include: "rules/baysor/run/baysor.smk"
include: "rules/baysor/postprocess/baysorpostprocess.smk"

df = pd.read_csv(config["samples"],sep=",", header=0)
samples = df.loc[:,'sample']
nuclear_dict = df.set_index('sample').to_dict()['nuclear_image']
spot_table = df.set_index('sample').to_dict()['spot_table']

for _, row in df.iterrows():
    if (not os.path.exists(row['nuclear_image']) 
        or not os.path.exists(row['spot_table'])):
        raise FileNotFoundError(f"{row['nuclear_image']} or {row['spot_table']} doesn't exist")
        

def get_nuclear_image_file(wildcards):
    return nuclear_dict[wildcards.sample]

def get_spot_table_file(wildcards):
    return spot_table[wildcards.sample]

rule all:
    input:
        expand("{result_dir}/baysor/run/{sample}/baysor_counts.csv",sample=samples,result_dir=config['result_dir'])
        
rule nuclear_image_link_out:
    input:
        get_nuclear_image_file
    output:
        "{result_dir}/link_out_nuclearimage/{sample}.nuclear_image.tiff"
    shell:
        """
        ln -s {input} {output}
        """

rule spot_table_link_out:
    input:
        get_spot_table_file
    output:
        "{result_dir}/link_out_spottable/{sample}.spot_table.csv"
    shell:
        """
        ln -s {input} {output}
        """
