import os
from snakemake import shell

cellxgene = os.path.join(
	os.path.dirname(__file__),
	"cellxgene.py",
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

python {cellxgene} \
	-s {snakemake.input.segmentations_csv} \
	--output_cellxgene {snakemake.output.cellxgene} \
	--output_polygon {snakemake.output.polygon}
"""
)