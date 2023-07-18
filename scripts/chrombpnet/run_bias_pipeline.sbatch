#!/bin/bash
#SBATCH --job-name=bias_pipeline   # Job name
#SBATCH --gres=gpu:1            # Number of GPUs required
#SBATCH --mem=100GB             # Memory requirement per node
#SBATCH --time=24:00:00         # Time limit in HH:MM:SS format
#SBATCH --output=output_%j.log  # Output file with job number in the filename
#SBATCH --error=output_%j.log
#SBATCH --cpus-per-task=64

# Your job script commands go here
eval "$(conda shell.bash hook)"
conda activate chrombpnet

chrombpnet bias pipeline \
-ifrag /data/ceph/hdd/project/node_10/transcription_factor_activity/data/neurips/processed/all/separated/all_Erythroblast.tsv.gz \
-d "ATAC" -g /data/ceph/hdd/project/node_10/transcription_factor_activity/reference/refdata-cellranger-arc-GRCh38-2020-A-2.0.0/fasta/genome.fa \
-c /data/ceph/hdd/project/node_10/transcription_factor_activity/reference/refdata-cellranger-arc-GRCh38-2020-A-2.0.0/star/chrNameLength.txt \
-p /data/ceph/hdd/project/node_10/transcription_factor_activity/data/neurips/processed/all/separated/all_Erythroblast_peaks.narrowPeak \
-n /data/ceph/hdd/project/node_10/transcription_factor_activity/data/neurips/processed/all/separated/all_Erythroblast_negatives.bed \
-fl /s/project/transcription_factor_activity/data/neurips/processed/s1d1/chrombpnet/splits/fold_0.json \
-b 0.5 \
-o /data/ceph/hdd/project/node_10/transcription_factor_activity/data/neurips/processed/all/chrombpnet/Erythroblast
