## Informatikos kurso Operacinių sistemų laboratorinis darbas.

Autoriai:

+ Linas Bisikirskas
+ Tomas Giedraitis

### Setup environment (linux)
```
python3 -m venv env
source env/bin/activate
./env/bin/python3 -m pip install --upgrade pip
```

### Run tests
* first, go into the directory where test.py is located
`cd OS/Emulator/pyemu/`

* then run tests using one of the commands below
```
python test.py
python -v test.py     # (verbose)
python -m unittest test.py
python -m unittest test.Utils
python -m unittest test.Utils.test_unicode_str
```
