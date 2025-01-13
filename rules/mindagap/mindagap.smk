rule pull_mindagap_container:
    params:
        link=config['containers']['mindagap']
    output:
        "{result_dir}/containers/mindagap/mindagap_002.sif"
    resources:
        threads=2,
        memory="6G"
    shell:
        """
        apptainer pull {output} {params.link}
        """

rule mindagap_removegap:
    input:
        container="{result_dir}/containers/mindagap/mindagap_002.sif",
        tif="{result_dir}/link_out_nuclearimage/{sample}.nuclear_image.tiff"
    output:
        "{result_dir}/mindagap/{sample}_gridfilled.tiff"
    params:
        xt=2144
    resources:
        threads=4,
        memory="8G"
    shell:
        """
        op_tmp=$(echo {input.tif} | cut -d '.' -f 1,2)
        cmd="mindagap.py {input.tif} \
            -xt {params.xt}"
        original_file=$(readlink {input.tif})
        dir_files=$(dirname {input.tif})
        apptainer exec --home $PWD \
            -B $dir_files:$dir_files \
            -B $original_file:$original_file \
            -B {input.tif}:{input.tif} \
            {input.container} $cmd
        mv ${{op_tmp}}_gridfilled.tiff {output}
        """

rule mindagap_removeDuplicate:
    input:
        container="{result_dir}/containers/mindagap/mindagap_002.sif",
        spot_table="{result_dir}/link_out_spottable/{sample}.spot_table.csv"
    output:
        "{result_dir}/mindagap/{sample}_markedDups.txt"
    resources:
        threads=4,
        memory="6G"
    shell:
        r"""
        op_tmp=$(echo {input.spot_table} | cut -d '.' -f 1,2)
        cmd="duplicate_finder.py {input.spot_table}"
        original_file=$(readlink {input.spot_table})
        dir_files=$(dirname {input.spot_table})
        apptainer exec --home $PWD \
            -B $dir_files:$dir_files \
            -B $original_file:$original_file \
            -B {input.spot_table}:{input.spot_table} \
            {input.container} $cmd
        mv ${{op_tmp}}_markedDups.txt {output}
        """