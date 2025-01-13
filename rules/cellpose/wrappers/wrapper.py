from snakemake import shell

config = snakemake.config['segmentation']['cellpose']

shell.executable("/bin/bash")

cellpose_model_path=config['models_path']
diameter=config['diameter']
flow_threshold=config['flow_threshold']
pretrained_model=config['pretrained_model']
shell(
    r"""
# -----------------------------------------------------------------------------
# Redirect stderr to log file by default and enable printing executed commands
# Also pipe stderr to log file
if [[ -n "{snakemake.log.log}" ]]; then
    if [[ "$(set +e; tty; set -e)" != "" ]]; then
        rm -f "{snakemake.log.log}" && mkdir -p $(dirname {snakemake.log.log})
        exec 2> >(tee -a "{snakemake.log.log}" >&2)
    else
        rm -f "{snakemake.log.log}" && mkdir -p $(dirname {snakemake.log.log})
        echo "No tty, logging disabled" >"{snakemake.log.log}"
    fi
fi

export CELLPOSE_LOCAL_MODELS_PATH={cellpose_model_path}
out_dir=$(dirname {snakemake.output.mask})
ip_dir=$(dirname {snakemake.input.img})
cellpose --verbose \
--diameter {diameter} \
--flow_threshold {flow_threshold} \
--image_path {snakemake.input.img} \
--pretrained_model {pretrained_model} \
--save_rois \
--save_tif \
--savedir $out_dir
mv $ip_dir/{snakemake.wildcards.sample}_gridfilled_rois.zip {snakemake.output.rois}
"""
)
