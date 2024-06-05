# MRI .pdf report creator

to use:

0. supply your own `data.json` to `src/data/` or use included one
1. create python venv and install deps
```bash
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
```
2. create `index.html` from template (dotn forget to activate python env)
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
