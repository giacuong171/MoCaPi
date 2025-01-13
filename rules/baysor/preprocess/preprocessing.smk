rule spots2cell:
    input:
        mask="{result_dir}/segmentation/cellpose/{sample}_gridfilled_cp_masks.tif",
        spot_table="{result_dir}/mindagap/{sample}_markedDups.txt",
    output:
        # spots2cell="{result_dir}/baysor/preprocessing/{sample}_cp_spots2cell.csv",
        spottable="{result_dir}/baysor/preprocessing/{sample}/{sample}_markedDups.csv",
        ratio="{result_dir}/baysor/preprocessing/{sample}/{sample}_genesRatio.csv",
    resources:
        memory="10G"
    log:
        log="{result_dir}/baysor/preprocessing/log/{sample}/spot2cell/{sample}_spot2cell.log"
    wrapper:
        "file:rules/baysor/preprocess/spots2cell/"

rule CreateConfig:
    input:
        ratio_file="{result_dir}/baysor/preprocessing/{sample}/{sample}_genesRatio.csv"
    output:
        config_toml="{result_dir}/baysor/preprocessing/{sample}/config.toml"
    log:
        log="{result_dir}/baysor/preprocessing/log/{sample}/createconfig/createconfig.log"
    wrapper:
        "file:rules/baysor/preprocess/createconfig/"