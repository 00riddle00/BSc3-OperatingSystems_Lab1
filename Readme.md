
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
buildout bootstrap
make buildout
```

### Run Emulator
```
cd code/Emulator/
source env/bin/activate
make run
```

### Run tests

```
cd code/Emulator/
source env/bin/activate
make test
```

### PyCharm setup
* Build project (see above). Then:
    * enable Buildout Support -> use paths from script: `code/Emulator/bin/buildout`
    * set up Python interpreter as `code/Emulator/bin/python-interpreter` instead of `code/Emulator/env/bin/python`
