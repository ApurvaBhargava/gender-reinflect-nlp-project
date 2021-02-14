#!/bin/bash
#SBATCH -p nvidia 
# use gpus
#SBATCH --gres=gpu:1
# memory
#SBATCH --mem=20GB
# Walltime format hh:mm:ss
#SBATCH --time=11:30:00
# Output and error files
#SBATCH -o job.%J.out
#SBATCH -e job.%J.err

nvidia-smi
module purge

export DATA_DIR=/scratch/ba63/nlp-project-2020/data/splits/

python main.py \
 --data_dir $DATA_DIR \
 --embed_trg_gender \
 --trg_gender_embedding_dim 10 \
 --embedding_dim 128 \
 --hidd_dim 256 \
 --num_layers 2 \
 --seed 21 \
 --model_path model.pt \
 --do_inference \
 --inference_mode dev \
 --preds_dir dev.preds.seq2seq.fr
