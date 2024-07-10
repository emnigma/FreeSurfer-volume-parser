# MRI .pdf report creator

//TODO

# Creating source data

//TODO

## Docker

To parse FreeSurfer subjects (`<subj>/stats` dir is sufficient) using `asegstats2table` and `aparcstats2table`, one can use FreeSurfer docker image to use these commands more easily. To access these commands, do:

```bash
# supply your own `license.txt` to project root dir to build container
docker build -t fscontainer .
docker run -v <SUBJECTS_DIR>:/root/data -it --rm fscontainer /bin/bash

$> cd data
$> asegstats2table --subjects $subject_id --meas volume --tablefile $subject_id/aseg_volume.csv
$> ...
$> exit

python3 analyze_dir.py <SUBJECTS_DIR> <anydest>
```

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
