export SUBJECTS_DIR=$1

SUBJECT_NAME=$2
LICENSE_PATH=$3
OUTDIR=$4

mkdir $OUTDIR

ASEG_APARC_OUTPUT=$OUTDIR/aseg_aparc_output
VOLUMES_JSON_OUTPUT=$OUTDIR/volumes_json_output
REPORT_GEN_OUTPUT=$OUTDIR/report_gen_output
FS_IMAGE=freesurfer/freesurfer:7.1.1

mkdir $ASEG_APARC_OUTPUT

docker run -v $LICENSE_PATH:/usr/local/freesurfer/.license \
    -v ./$ASEG_APARC_OUTPUT:/output \
    -v $SUBJECTS_DIR/$SUBJECT_NAME:/usr/local/freesurfer/subjects/subj \
    -it --rm $FS_IMAGE asegstats2table \
    --subjects subj \
    --meas volume \
    --tablefile /output/aseg_volume.csv

docker run -v $LICENSE_PATH:/usr/local/freesurfer/.license\
    -v ./$ASEG_APARC_OUTPUT:/output \
    -v $SUBJECTS_DIR/$SUBJECT_NAME:/usr/local/freesurfer/subjects/subj \
    -it --rm $FS_IMAGE aparcstats2table \
    --subjects subj \
    --hemi lh \
    --meas volume \
    --tablefile /output/aparc_lh_volume.csv

docker run -v $LICENSE_PATH:/usr/local/freesurfer/.license \
    -v ./$ASEG_APARC_OUTPUT:/output \
    -v $SUBJECTS_DIR/$SUBJECT_NAME:/usr/local/freesurfer/subjects/subj \
    -it --rm $FS_IMAGE aparcstats2table \
    --subjects subj \
    --hemi rh \
    --meas volume \
    --tablefile /output/aparc_rh_volume.csv

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

yarn install
yarn run dev &

python3 convert.py $REPORT_GEN_OUTPUT

killall -9 node
