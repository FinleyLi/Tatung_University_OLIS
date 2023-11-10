# Install virtualenv
python -m pip install --upgrade pip # upgrade pip
pip install virtualenv

# Build
py -0     # list all installed packages
py -3.11 -m venv Env3116 # create virtual environment
```
(python -m virtualenv venv01)
(virtualenv venv --python=python3.8)
```

# active
linux
- source ./venv01/bin/activate
win cmd
- .\venv\Scripts\activate.bat
win powershell
- .\venv\Scripts\activate.ps1

- deactivate # exit

--------------------
Package    Version
---------- -------

# Output/Input packages info
- pip freeze > requirements.txt
- pip install -r requirements.txt