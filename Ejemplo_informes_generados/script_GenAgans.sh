#!/bin/bash

mkdir 1.Analisis_calidad

fastqc -o 1.Analisis_calidad/ SRR14695036_1.fastq.gz SRR14695036_2.fastq.gz

mkdir 2.Lecturas_limpias





fastp -i SRR14695036_1.fastq.gz -I SRR14695036_2.fastq.gz                 -o ./2.Lecturas_limpias/SRR14695036_1_clean.fq.gz                 -O ./2.Lecturas_limpias/SRR14695036_2_clean.fq.gz                 --cut_tail 15 --cut_front 15 --cut_mean_quality                 30 --detect_adapter_for_pe --trim_poly_g --trim_poly_x -l                 100                 -h ./2.Lecturas_limpias/SRR14695036_1_SRR14695036_2_fastp.html                 -j ./2.Lecturas_limpias/SRR14695036_1_SRR14695036_2_fastp.json

mkdir 3.Genoma_referencia_indexado

cp Homo_sapiens.GRCh37.dna.chromosome.1.fa ./3.Genoma_referencia_indexado/Homo_sapiens.GRCh37.dna.chromosome.1.fa

bwa index -p ./3.Genoma_referencia_indexado/Homo_sapiens.GRCh37.dna.chromosome.1.fa                             ./3.Genoma_referencia_indexado/Homo_sapiens.GRCh37.dna.chromosome.1.fa

mkdir 4.Mapeo

bwa mem -a ./3.Genoma_referencia_indexado/Homo_sapiens.GRCh37.dna.chromosome.1.fa                             ./2.Lecturas_limpias/SRR14695036_1_clean.fq.gz                             ./2.Lecturas_limpias/SRR14695036_2_clean.fq.gz                             -o ./4.Mapeo/mapeo.sam

mkdir 5.Analisis_mapeo

samtools view -bS ./4.Mapeo/mapeo.sam -o ./5.Analisis_mapeo/mapeo.bam

samtools sort ./5.Analisis_mapeo/mapeo.bam -o ./5.Analisis_mapeo/mapeo_sorted.bam

samtools stats ./5.Analisis_mapeo/mapeo_sorted.bam > ./5.Analisis_mapeo/analisis_mapeo.txt

plot-bamstats -p ./5.Analisis_mapeo/informe_mapeo ./5.Analisis_mapeo/analisis_mapeo.txt

mkdir 6.Limpieza_duplicados

picard MarkDuplicates --INPUT ./5.Analisis_mapeo/mapeo_sorted.bam                               --OUTPUT ./6.Limpieza_duplicados/mapeo_dedup.bam                               --METRICS_FILE ./6.Limpieza_duplicados/MarkDuplicatesMetrics.txt                               --ASSUME_SORTED True

samtools view -H ./6.Limpieza_duplicados/mapeo_dedup.bam | grep "^@RG" > ./6.Limpieza_duplicados/ReadGroups.txt

mv ./6.Limpieza_duplicados/mapeo_dedup.bam ./6.Limpieza_duplicados/mapeo_dedup_copy.bam

picard AddOrReplaceReadGroups -I ./6.Limpieza_duplicados/mapeo_dedup_copy.bam                               -O ./6.Limpieza_duplicados/mapeo_dedup.bam                               -RGID default                               -RGLB lib1                               -RGPL ILLUMINA                               -RGSM sample1                               -RGPU unit1

mkdir 7.Llamada_variantes

mv Homo_sapiens.GRCh37.dna.chromosome.1.fa ./7.Llamada_variantes/Homo_sapiens.GRCh37.dna.chromosome.1.fa

samtools faidx ./7.Llamada_variantes/Homo_sapiens.GRCh37.dna.chromosome.1.fa

samtools index ./6.Limpieza_duplicados/mapeo_dedup.bam

freebayes --ploidy 2                               --min-alternate-fraction 0.3                               --min-alternate-count 100                               --min-mapping-quality 30                                                              -f ./7.Llamada_variantes/Homo_sapiens.GRCh37.dna.chromosome.1.fa                               ./6.Limpieza_duplicados/mapeo_dedup.bam > ./7.Llamada_variantes/variantes.vcf

rtg vcfstats ./7.Llamada_variantes/variantes.vcf > ./7.Llamada_variantes/informe_variantes.txt

mkdir 8.Filtrado_variantes



cp ./7.Llamada_variantes/variantes.vcf ./7.Llamada_variantes/variantes_copy.vcf

vcftools --vcf ./7.Llamada_variantes/variantes_copy.vcf                             --recode --recode-INFO-all                             --out ./8.Filtrado_variantes/variantes.vcf                             --minQ 30                             --minDP 30                                                                                                                     

mv ./8.Filtrado_variantes/variantes.vcf.recode.vcf ./8.Filtrado_variantes/variantes.vcf

rtg vcfstats ./8.Filtrado_variantes/variantes.vcf > ./8.Filtrado_variantes/informe_variantes_filtradas.txt

mkdir 9.Efecto_variantes

vep -i ./8.Filtrado_variantes/variantes.vcf                             -o ./9.Efecto_variantes/efecto_variantes.tsv                             --database --species homo_sapiens --force_overwrite --tab                             --assembly GRCh37                             --sift b                             --polyphen b                             --check_existing                             --uniprot                             --af                                                                                        