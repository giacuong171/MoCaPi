rule pull_baysor_container:
    params:
        link=config['containers']['baysor']
    output:
        "{result_dir}/containers/baysor/baysor_062.sif"
    resources:
        threads=4,
        memory="4G"
    shell:
        """
        apptainer pull {output} {params.link}
        """

rule baysor:
    input:
        container="{result_dir}/containers/baysor/baysor_062.sif",
        spottable="{result_dir}/baysor/preprocessing/{sample}/{sample}_markedDups.csv",
        # mask="{result_dir}/segmentation/cellpose/{sample}_gridfilled_cp_masks.tif",
        config_toml="{result_dir}/baysor/preprocessing/{sample}/config.toml"
    output:
        segmentation_stat = "{result_dir}/baysor/run/{sample}/segmentation_cell_stats.csv",
        segmentations_csv = "{result_dir}/baysor/run/{sample}/segmentation.csv",
        loom_file = "{result_dir}/baysor/run/{sample}/segmentation_counts.loom",
    log:
        log="{result_dir}/baysor/run/log/{sample}_baysor.log"
    resources:
        threads=6,
        memory="100G"
    wrapper:
        "file:rules/baysor/run/wrappers/"

