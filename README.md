# MRI .pdf and web-page report creator

## Running pipeline

1. Install `freesurfer/freesurfer:7.1.1` docker image
2. Obtain FreeSurfer `license.txt`
3. Run the following command:
```bash
bash pipeline.sh <ABS_SUBJECT_DIR> <SUBJECT_NAME> <ABS_PATH_TO_FILE_WITH_LICENSE> <OUTDIR>
```

# Details

## Parsing and analysis with Docker

One way to parse FreeSurfer subjects (`<subj>/stats` dir is sufficient) using `asegstats2table` and `aparcstats2table`, one can use FreeSurfer docker image to use these commands more easily. To access these commands, do:

```bash
# supply your own `license.txt` to project root dir to build container
docker run -v <SUBJECTS_DIR>:/root -it --rm freesurfer/freesurfer:7.1.1 /bin/bash

$> asegstats2table ...
$> aparcstats2table ...
$> exit

python3 analyze_dir.py <SUBJECTS_DIR> <anydest>
```

<details>
   <summary>Auto parse subject by id</summary>

   ```bash
   subject_id=$1

   export SUBJECTS_DIR="./"

   # Step 1: Extract Subcortical Volumes
   asegstats2table --subjects $subject_id --meas volume --tablefile $subject_id/aseg_volume.csv

   # Step 2: Extract Cortical Volumes
   aparcstats2table --subjects $subject_id --hemi lh --meas volume --tablefile $subject_id/aparc_lh_volume.csv
   aparcstats2table --subjects $subject_id --hemi rh --meas volume --tablefile $subject_id/aparc_rh_volume.csv
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
