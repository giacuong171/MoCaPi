import os
from snakemake import shell

spot2cell = os.path.join(
	os.path.dirname(__file__),
	"assign_spotcell.py",
)
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

python {spot2cell} \
	-s {snakemake.input.spot_table} \
	-c {snakemake.input.mask} \
	--output_spot_table {snakemake.output.spottable} \
	--output_ratio {snakemake.output.ratio}
"""
)