rule identify_species_fastq:
    input:
        r1=OUT + "/clean_fastq/{sample}_pR1.fastq.gz",        
        r2=OUT + "/clean_fastq/{sample}_pR2.fastq.gz"
    output:
        kraken2_kreport = OUT + '/identify_species_fastq/{sample}.kreport2',
        bracken_s = OUT + '/identify_species_fastq/{sample}_species_content.txt',
        bracken_kreport = OUT + '/identify_species_fastq/{sample}_bracken_species.kreport2'
    log:
        OUT + '/log/identify_species_fastq/{sample}_fastq.log'
    threads: 
        config["threads"]["kraken2"]
    conda:
        '../../envs/identify_species.yaml'
    container:
        'library://alesr13/default/kraken2_bracken:v2.1.2_v2.6.1'
    params:
        kraken_db=config["db_dir"]
    resources:
        mem_gb=config["mem_gb"]["kraken2"]
    shell:
        """
# Adding --confidence 0.05 causes 0 kmers assigned to species in some samples
# That breaks bracken
kraken2 --db {params.kraken_db} \
    --threads {threads} \
    --report {output.kraken2_kreport} \
    --fastq-input {input}  &> {log} 

bracken -d {params.kraken_db} \
    -i {output.kraken2_kreport} \
    -o {output.bracken_s} \
    -r 150 \
    -l S \
    -t 0  &>> {log} 

        """

rule top_species_multireport_fastq:
    input: 
        expand(OUT + '/identify_species_fastq/{sample}_species_content.txt', sample = SAMPLES)
    output:
        OUT + '/identify_species_fastq/top1_species_multireport.csv'
    log:
        OUT + '/log/identify_species_fastq/multireport.log'
    threads: 
        config["threads"]["parsing"]
    resources:
        mem_gb=config["mem_gb"]["parsing"]
    shell:
        """
python bin/make_summary_main_species.py --input-files {input} \
                                        --output-multireport {output} > {log}
        """
