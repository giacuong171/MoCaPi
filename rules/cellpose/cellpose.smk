
rule cellpose_segmentation:
    input:
        img="{result_dir}/mindagap/{sample}_gridfilled.tiff"
    output:
        rois="{result_dir}/segmentation/cellpose/{sample}_gridfilled_rois.zip",
        mask="{result_dir}/segmentation/cellpose/{sample}_gridfilled_cp_masks.tif"
    log:
        log="{result_dir}/segmentation/cellpose/log/{sample}_cp.log"
    resources:
        threads=4,
        memory="50G"
    wrapper:
        "file:rules/cellpose/wrappers/"
