# this is preparation of enviroment for test automation (working with python 3.13)
# HELP: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r .\requirments.txt
pip freeze > requirments.txt