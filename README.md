# MRI .pdf and web-page report creator

## Running pipeline

#### Run pipeline manually
Run the following command:
```bash
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
bash pipeline.sh <ABS_SUBJECT_DIR> <SUBJECT_NAME> <JSON_METADATA> <OUTDIR>

yarn install
yarn dev run &
python3 convert.py <PDF_REPORT_SAVEPATH>
```

#### Run pipeline using docker
or use container from dockerhub. in this case you dont need python env to generate `index.html`
```bash
docker run \
    -v <ABS_SUBJECT_DIR>/<SUBJECT_NAME>:/root/data \
    -v <ABS_OUTDIR>:/root/out \
    -v <JSON_METADATA>:/root/data/metadata.json \
    -it --rm neurographx-mri-pages-vis:latest /root/data <SUBJECT_NAME> /root/data/metadata.json /root/out

python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
yarn install
yarn dev run &
python3 convert.py <PDF_REPORT_SAVEPATH>
```
(!) `SUBJECTS_DIR` should be set to dir with fs-subjects

Your output directory will look like this:
```
<OUTDIR>/
├── aseg_aparc_output/
│   ├── aparc_lh_volume.csv
│   ├── aparc_rh_volume.csv
│   └── aseg_volume.csv
├── report_gen_output/
│   └── index.html
└── volumes_json_output/
    └── data.json
```
# Details

## Manual parsing and analysis

To parse FreeSurfer subjects (`<subj>/stats` dir is sufficient) using `asegstats2table` and `aparcstats2table`, one can use provided FreeSurfer python scripts. To access these commands, do:

```bash

$ pysurfer/asegstats2table.py ...
$ pysurfer/aparcstats2table.py ...

$ python3 analyze_dir.py <SUBJECTS_DIR> <anydest>
```

<details>
   <summary>Auto parse subject by id</summary>

   ```bash
   subject_id=$1

   export SUBJECTS_DIR="./"

   # Step 1: Extract Subcortical Volumes
   pysurfer/asegstats2table.py --subjects $subject_id --meas volume --tablefile $subject_id/aseg_volume.csv

   # Step 2: Extract Cortical Volumes
   pysurfer/aparcstats2table.py --subjects $subject_id --hemi lh --meas volume --tablefile $subject_id/aparc_lh_volume.csv
   pysurfer/aparcstats2table.py --subjects $subject_id --hemi rh --meas volume --tablefile $subject_id/aparc_rh_volume.csv
   ```

</details>

# Parser theory

To accurately calculate the volumes of the Frontal, Temporal, Occipital, and Parietal cortexes from the FreeSurfer output, we need to sum the relevant regions associated with each cortex. Data for this separation is sourced from [Desikan-Killiany atlas](https://surfer.nmr.mgh.harvard.edu/ftp/articles/desikan06-parcellation.pdf):

### Volumes Calculation

1. **Frontal Cortex Volumes:**
   - Superior frontal gyrus: superiorfrontal_volume
   - Middle frontal gyrus:
     - Rostral division: rostralmiddlefrontal_volume
     - Caudal division: caudalmiddlefrontal_volume
   - Inferior frontal gyrus:
     - Pars opercularis: parsopercularis_volume
     - Pars triangularis: parstriangularis_volume
     - Pars orbitalis: parsorbitalis_volume
   - Orbitofrontal cortex:
     - Lateral division: lateralorbitofrontal_volume
     - Medial division: medialorbitofrontal_volume
   - Frontal pole: frontalpole_volume
   - Precentral gyrus: precentral_volume
   - Paracentral lobule: paracentral_volume

2. **Temporal Cortex Volumes:**
   - Temporal lobe—medial aspect
      - Entorhinal cortex: entorhinal_volume
      - Parahippocampal gyrus: parahippocampal_volume
      - Temporal pole: temporalpole_volume
      - Fusiform gyrus: fusiform_volume
   - Temporal lobe—lateral aspect
      - Superior temporal gyrus: superiortemporal_volume
      - Middle temporal gyrus: middletemporal_volume
      - Inferior temporal gyrus: inferiortemporal_volume
      - Transverse temporal cortex: transversetemporal_volume
      - Banks of the superior temporal sulcus: bankssts_volume

3. **Occipital Cortex Volumes:**
   - Lingual gyrus: lingual_volume
   - Pericalcarine cortex: pericalcarine_volume
   - Cuneus cortex: cuneus_volume
   - Lateral occipital cortex: lateraloccipital_volume

4. **Parietal Cortex Volumes:**
   - Postcentral gyrus: postcentral_volume
   - Supramarginal gyrus: supramarginal_volume
   - Superior parietal cortex: superiorparietal_volume
   - Inferior parietal cortex: inferiorparietal_volume
   - Precuneus cortex: precuneus_volume
