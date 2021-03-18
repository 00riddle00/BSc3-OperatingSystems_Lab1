## Informatikos kurso Operacinių sistemų laboratorinis darbas.

Autoriai:

+ Linas Bisikirskas
+ Tomas Giedraitis

### Setup environment (linux)
```
python3 -m venv env
source env/bin/activate
./env/bin/python3 -m pip install --upgrade pip
./env/bin/python3 -m pip install -r requirements.txt
```

### Run tests
```
python test.py
python -v test.py     # (verbose)
python -m unittest test.py
python -m unittest test.Utils
python -m unittest test.Utils.test_unicode_str
```
