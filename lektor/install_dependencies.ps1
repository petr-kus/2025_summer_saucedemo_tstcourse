python -m venv venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\venv\Scripts\activate.ps1
pip install -r requirements.txt
pip freeze > requirements.txt