# How to use
This exemplary piece of Python code, show how to use [API of Gdańskie Wody](https://pomiary.gdanskiewody.pl/). 
Through this API meteorological data can be downloaded and further analyzed.
It is required to make a free account, and get personal API key.

When API key is known, then below steps guide to build small app, 
which prints in the console meteorological data of Gdańsk area

## Virtual environment
If you do not have venv for specific python version then firstly install it:
```commandline
sudo apt-get install python3.10-venv
```
Above command works on Ubuntu, for Windows go e.g. with this [tutorial](https://www.geeksforgeeks.org/creating-python-virtual-environment-windows-linux/)

After that, create your python virtual environment:
```commandline
python3.10 -m venv .env
source .env/bin/activate
```

## Requirements
Base requirements are listed in `requirements.txt`, and they are enough to run the app. They can be installed via:
```commandline
pip install -r requirements.txt
```
If you want to change the code, then it is recommended to install helper libraries for better code maintenance 
```commandline
pip install -r dev-requirements.txt
```
Or both at once:
```commandline
pip install -r requirements.txt -r dev-requirements.txt
```

## Run
```commandline
python main.py
```

## Code maintenance
If you want to make code standardized, install `dev-requirements.txt`, and use those libs, e.g.:
```commandline
isort --profile black main.py
black main.py
pylint main.py
```