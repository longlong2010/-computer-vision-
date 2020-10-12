python3 export_inference_graph.py \
    --input_type=image_tensor \
    --pipeline_config_path=training/ssd_mobilenet_v2_coco.config \
    --trained_checkpoint_prefix=training/model.ckpt-15000 \
    --output_directory=result
