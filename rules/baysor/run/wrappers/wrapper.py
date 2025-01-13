import os
from snakemake import shell

config = snakemake.config['segmentation']['baysor']
op_dir = os.path.dirname(snakemake.output.segmentations_csv)
files_to_bind = {
    "spottable": snakemake.input.spottable,
    "config_file": snakemake.input.config_toml,
    "op_dir": op_dir,
}
files_to_bind = {k: os.path.realpath(v) for k, v in files_to_bind.items()}
dirs_to_bind = {k: os.path.dirname(v) for k, v in files_to_bind.items()}
bound_dirs = {e[1]: e[0] for e in enumerate(list(set(dirs_to_bind.values())))}
bindings = " ".join(["-B {}:/bindings/d{}".format(k, v) for k, v in bound_dirs.items()])
bound_files = {
    k: "/bindings/d{}/{}".format(bound_dirs[dirs_to_bind[k]], os.path.basename(v))
    for k, v in files_to_bind.items()
}

n_clusters = config["n-clusters"]
prior_segmentation_confidence = config["prior-segmentation-confidence"]
if config["no-ncv-estimation"] == True:
    no_ncv_estimation="--no-ncv-estimation"
else:
    no_ncv_estimation=""

shell.executable("/bin/bash")

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

# Setup auto-cleaned tmpdir
export TMPDIR=$(mktemp -d)
trap "rm -rf $TMPDIR" EXIT

cmd="baysor run {no_ncv_estimation} \
--n-clusters={n_clusters} \
--prior-segmentation-confidence {prior_segmentation_confidence} \
-m 3 -c {bound_files[config_file]} \
-o {bound_files[op_dir]} \
{bound_files[spottable]} \
:cell"
echo 'JULIA_NUM_THREADS={snakemake.resources.threads}' > $TMPDIR/{snakemake.wildcards.sample}.sh
echo $cmd >> $TMPDIR/{snakemake.wildcards.sample}.sh
apptainer exec --home $PWD -B $TMPDIR:/bindings/d5 {bindings} {snakemake.input.container} bash /bindings/d5/{snakemake.wildcards.sample}.sh
"""
)