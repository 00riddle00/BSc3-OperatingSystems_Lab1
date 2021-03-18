
## Informatikos kurso Operacinių sistemų laboratorinis darbas.

Autoriai:

+ Linas Bisikirskas
+ Tomas Giedraitis

### Setup environment (linux)
```
cd code/Emulator/
python3 -m venv env
source env/bin/activate
./env/bin/python3 -m pip install --upgrade pip
./env/bin/python3 -m pip install -r requirements.txt
```
### Build project
```
cd code/Emulator/
source env/bin/activate
buildout
```

### Run simulation
```
cd code/Emulator/
source env/bin/activate
make run
```

### Run tests

#### the preferred way
```
cd code/Emulator/
source env/bin/activate
make test
```

#### (the old way)
* first, go into the directory where test.py is located
`cd code/Emulator/pyemu/`

* then run tests using one of the commands below
```
python test.py
python -v test.py     # (verbose)
python -m unittest test.py
python -m unittest test.Utils
python -m unittest test.Utils.test_unicode_str
```
