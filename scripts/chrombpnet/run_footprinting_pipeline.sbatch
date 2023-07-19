#!/bin/bash
#SBATCH --job-name=footprinting_pipeline   # Job name
#SBATCH --gres=gpu:1            # Number of GPUs required
#SBATCH --mem=40GB             # Memory requirement per node
#SBATCH --time=04:00:00         # Time limit in HH:MM:SS format
#SBATCH --output=output_%j.log  # Output file with job number in the filename
#SBATCH --error=output_%j.log
#SBATCH --cpus-per-task=20

# Your job script commands go here
eval "$(conda shell.bash hook)"
conda activate chrombpnet

chrombpnet footprints \
-m /data/ceph/hdd/project/node_10/transcription_factor_activity/data/neurips/processed/all/chrombpnet/Erythroblast/models/chrombpnet_nobias.h5 \
-g /data/ceph/hdd/project/node_10/transcription_factor_activity/reference/refdata-cellranger-arc-GRCh38-2020-A-2.0.0/fasta/genome.fa \
-r /data/ceph/hdd/project/node_10/transcription_factor_activity/data/neurips/processed/all/separated/all_Erythroblast_negatives.bed \
-fl /s/project/transcription_factor_activity/data/neurips/processed/s1d1/chrombpnet/splits/fold_0.json \
-o /data/ceph/hdd/project/node_10/transcription_factor_activity/data/neurips/processed/all/chrombpnet/Erythroblast/footprinting \
-pwm_f /data/ouga/home/ag_gagneur/martensl/github_repos/transcription_factor_activity/scripts/chrombpnet/motif_to_pwm.TF.tsv
