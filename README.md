# MRI .pdf report creator

to use:

0. supply your own `data.json` to `src/data/` or use included one
1. create python venv and install deps
```bash
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
```
2. create `index.html` from template (don't forget to activate python env)
```bash
cd src && python3 main.py && cd -
```
3. install yarn and host index.html
```bash
yarn dev src/index.html
```
4. generate .pdf page
```bash
python3 pdfy.py
```

# Creating source data

//TODO

# Parser theory

To accurately calculate the volumes of the Frontal, Temporal, Occipital, and Parietal cortexes from the FreeSurfer output, we need to sum the relevant regions associated with each cortex:

### Volumes Calculation

1. **Frontal Cortex Volumes:**
   - lh_caudalmiddlefrontal_volume
   - lh_lateralorbitofrontal_volume
   - lh_medialorbitofrontal_volume
   - lh_parsopercularis_volume
   - lh_parsorbitalis_volume
   - lh_parstriangularis_volume
   - lh_precentral_volume
   - lh_rostralmiddlefrontal_volume
   - lh_superiorfrontal_volume
   - lh_frontalpole_volume

2. **Temporal Cortex Volumes:**
   - lh_entorhinal_volume
   - lh_fusiform_volume
   - lh_inferiortemporal_volume
   - lh_middletemporal_volume
   - lh_parahippocampal_volume
   - lh_superiortemporal_volume
   - lh_temporalpole_volume
   - lh_transversetemporal_volume

3. **Occipital Cortex Volumes:**
   - lh_cuneus_volume
   - lh_lateraloccipital_volume
   - lh_lingual_volume
   - lh_pericalcarine_volume

4. **Parietal Cortex Volumes:**
   - lh_inferiorparietal_volume
   - lh_isthmuscingulate_volume
   - lh_postcentral_volume
   - lh_precuneus_volume
   - lh_superiorparietal_volume
   - lh_supramarginal_volume
   - lh_paracentral_volume
