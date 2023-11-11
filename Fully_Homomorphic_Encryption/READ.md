# step by step to install tenseal on windows 10
py -0     # list all installed packages
python -m pip install --upgrade pip # upgrade pip
py -3.9 -m venv Env39FHE # create virtual environment

.\fhe39Env\Scripts\Activate.ps1
pip install tenseal
pip install numpy

--------------------
Package    Version
---------- -------
numpy      1.26.1
pip        22.0.4
setuptools 58.1.0
tenseal    0.3.14

# Output/Input packages info
- pip freeze > requirements.txt
- pip install -r requirements.txt