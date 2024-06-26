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
   - caudalmiddlefrontal_volume
   - lateralorbitofrontal_volume
   - medialorbitofrontal_volume
   - parsopercularis_volume
   - parsorbitalis_volume
   - parstriangularis_volume
   - precentral_volume
   - rostralmiddlefrontal_volume
   - superiorfrontal_volume
   - frontalpole_volume

2. **Temporal Cortex Volumes:**
   - entorhinal_volume
   - fusiform_volume
   - inferiortemporal_volume
   - middletemporal_volume
   - parahippocampal_volume
   - superiortemporal_volume
   - temporalpole_volume
   - transversetemporal_volume

3. **Occipital Cortex Volumes:**
   - cuneus_volume
   - lateraloccipital_volume
   - lingual_volume
   - pericalcarine_volume

4. **Parietal Cortex Volumes:**
   - inferiorparietal_volume
   - isthmuscingulate_volume
   - postcentral_volume
   - precuneus_volume
   - superiorparietal_volume
   - supramarginal_volume
   - paracentral_volume
