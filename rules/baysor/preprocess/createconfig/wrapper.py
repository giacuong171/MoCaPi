import os
from snakemake import shell

createConfig = os.path.join(
	os.path.dirname(__file__),
	"createconfig.py",
)

shell(
    r"""
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

    python {createConfig} --ratio_file {snakemake.input.ratio_file} \
        --config_toml {snakemake.output.config_toml}
        
"""
)