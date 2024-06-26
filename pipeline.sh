#!/bin/bash

# Calculate volumes and save to JSON
python3 pipeline.py calculate_volumes \
    --aseg .github/workflows/examples/aseg_volume.csv \
    --aparc_lh .github/workflows/examples/aparc_lh_volume.csv \
    --aparc_rh .github/workflows/examples/aparc_rh_volume.csv \
    --output-json data.json

yarn dev index.html &

python3 pipeline.py generate_html \
    --data-file data.json \
    --reference-data-file resources/reference_data.json \
    --template-dir resources/templates \
    --output-file index.html
