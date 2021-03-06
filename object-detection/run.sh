
python3 model_main.py \
    --pipeline_config_path=training/ssd_mobilenet_v2_coco.config \
    --model_dir=training \
    --num_train_steps=15000 \
    --num_eval_steps=2000 \
    --alsologtostderr
