export SUBJECTS_DIR=$1

SUBJECT_NAME=$2

# .json file
SUBJECT_METADATA=$3

# path to output dir
OUTDIR=$4

mkdir $OUTDIR

ASEG_APARC_OUTPUT="$OUTDIR/aseg_aparc_output"
VOLUMES_JSON_OUTPUT="$OUTDIR/volumes_json_output"
REPORT_GEN_OUTPUT="$OUTDIR/report_gen_output"

mkdir $ASEG_APARC_OUTPUT

python3 pysurfer/asegstats2table.py --subjects $SUBJECT_NAME --meas volume --tablefile $ASEG_APARC_OUTPUT/aseg_volume.csv
python3 pysurfer/aparcstats2table.py --subjects $SUBJECT_NAME --hemi lh --meas volume --tablefile $ASEG_APARC_OUTPUT/aparc_lh_volume.csv
python3 pysurfer/aparcstats2table.py --subjects $SUBJECT_NAME --hemi rh --meas volume --tablefile $ASEG_APARC_OUTPUT/aparc_rh_volume.csv

mkdir $VOLUMES_JSON_OUTPUT
python3 pipeline.py create_patient_data \
        --aseg $ASEG_APARC_OUTPUT/aseg_volume.csv \
        --aparc_lh $ASEG_APARC_OUTPUT/aparc_lh_volume.csv \
        --aparc_rh $ASEG_APARC_OUTPUT/aparc_rh_volume.csv \
        --metadata $SUBJECT_METADATA \
        --output-json $VOLUMES_JSON_OUTPUT/data.json 

mkdir $REPORT_GEN_OUTPUT

python3 pipeline.py generate_html \
        --data-file $VOLUMES_JSON_OUTPUT/data.json \
        --reference-data-file resources/reference_thickness.json \
        --template-dir resources/templates \
        --output-file $REPORT_GEN_OUTPUT/index.html
