# Python setup

Step 1. Install virtualenv
```
python -V
pip list
pip install --upgrade pip
pip install virtualenv
pip list
```
Step 2. Build
```
python -m virtualenv venv01
(virtualenv venv --python=python3.8)
```
Step 3. active
```
linux
source ./venv01/bin/activate
win cmd
.\venv\Scripts\activate.bat
win powershell
.\venv\Scripts\activate.ps1
```
Step 4. exit
```
deactivate
```
#### administrator use powershell type 
```
"set-executionpolicy remotesigned" Enter
```

# Output/Input packages info
- pip freeze > requirements.txt
- pip install -r requirements.txt
```
opencv-python==4.6.0.66
pdf2image==1.16.0
PyPDF2==2.11.1
pytesseract==0.3.10
```
#### System path
C:\Program Files Protable\poppler-0.68.0\bin
***https://tesseract-ocr.github.io/tessdoc/***
C:\Program Files\Tesseract-OCR\tessdata
C:\Program Files\Tesseract-OCR\
***https://poppler.freedesktop.org/***

# git setup

install git
```
	apt-get install git
	git --version
```

setup account
```
	git config --global user.name "<name>"
	git config --global user.email "<E-mail>"
```

add repository
```
	mkdir helloGit
	cd helloGit
	git init
	ls -la
```

watch status
	`git status`

clone SSH
	`git clone git@github.com:FinleyLi/109-TSH_Python_3.8.3.git`

clone HTTPS
	`git clone https://github.com/FinleyLi/109-TSH_Python_3.8.3.git`

select file
```
	cd /github/109.../
	git add README.md
	git commit -m 'add git use clone and push'
	git push
	username/mail
	password
```

error use `git pull`

# Sign

    print("    __ _       _                                        \n");
    print("   / _(_)_ __ | | ___ _   _                             \n");
    print("  | |_| |  _  | |/ _   | | |                            \n");
    print("  |  _| | | | | |  __/ |_| |                            \n");
    print("  |_| |_|_| |_|_||___|___  |                            \n");
    print("                      |___/                             \n");
    print("********************************************************\n");
    print("* E-mail_fnali@gm.ttu.edu.tw                           *\n");
    print("* Website_https://finleyli.medium.com/                 *\n");
    print("********************************************************\n");