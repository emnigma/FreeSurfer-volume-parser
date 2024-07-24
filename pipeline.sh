export SUBJECTS_DIR=$1

SUBJECT_NAME=$2
OUTDIR=$3

mkdir $OUTDIR

ASEG_APARC_OUTPUT=$OUTDIR/aseg_aparc_output
VOLUMES_JSON_OUTPUT=$OUTDIR/volumes_json_output
REPORT_GEN_OUTPUT=$OUTDIR/report_gen_output

mkdir $ASEG_APARC_OUTPUT

pysurfer/asegstats2table.py --subjects $SUBJECT_NAME --meas volume --tablefile $ASEG_APARC_OUTPUT/aseg_volume.csv
pysurfer/aparcstats2table.py --subjects $SUBJECT_NAME --hemi lh --meas volume --tablefile $ASEG_APARC_OUTPUT/aparc_lh_volume.csv
pysurfer/aparcstats2table.py --subjects $SUBJECT_NAME --hemi rh --meas volume --tablefile $ASEG_APARC_OUTPUT/aparc_rh_volume.csv

mkdir $VOLUMES_JSON_OUTPUT
python3 pipeline.py calculate_volumes \
        --aseg $ASEG_APARC_OUTPUT/aseg_volume.csv \
        --aparc_lh $ASEG_APARC_OUTPUT/aparc_lh_volume.csv \
        --aparc_rh $ASEG_APARC_OUTPUT/aparc_rh_volume.csv \
        --output-json $VOLUMES_JSON_OUTPUT/data.json 

mkdir $REPORT_GEN_OUTPUT
python3 pipeline.py generate_html \
        --data-file $VOLUMES_JSON_OUTPUT/data.json \
        --reference-data-file resources/reference_data.json \
        --template-dir resources/templates \
        --output-file $REPORT_GEN_OUTPUT/index.html

cp $REPORT_GEN_OUTPUT/index.html ./index.html

yarn install
yarn run dev &

python3 convert.py $REPORT_GEN_OUTPUT

killall -9 node
