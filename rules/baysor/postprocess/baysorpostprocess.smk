rule postprocess:
    input:
        segmentations_csv = "{result_dir}/baysor/run/{sample}/segmentation.csv",
    output:
        cellxgene="{result_dir}/baysor/run/{sample}/baysor_counts.csv",
        polygon = "{result_dir}/baysor/run/{sample}/baysor_cell_polygons.csv",
    resources:
        threads=2,
        memory="6G"
    log:
        log="{result_dir}/baysor/postprocess/log/{sample}_baysor.log"
    wrapper:
        "file:rules/baysor/postprocess/wrappers/"