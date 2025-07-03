# 2025_spring_saucedemo_tstcourse
Repository fortesting course spring 2025. 

## Related Documentation links
Documentation for Selenium 
https://selenium-python.readthedocs.io/getting-started.html
https://www.selenium.dev/documentation/

Documentation Locators in selenium 
https://selenium-python.readthedocs.io/locating-elements.html

Packages page:
https://pypi.org/

Documentation around virtual enviroments
https://docs.python.org/3/library/venv.html

Documentation Set-Execution policy 
https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.security/set-executionpolicy?view=powershell-7.4


## How to prepare virtual enviroment 
Windows 
Start Powershell command line as Administrator and use command 
```bash
Set-ExecutionPolicy –ExecutionPolicy RemoteSigned –Scope CurrentUser
```

Linux/MacOS
```bash
chmod +x setup.sh
./install_dependencies.sh
```

Start visual studio code (VS Code), open folder with your project and start from the terminal:
Windows 
```bash
.\install_dependencies.ps1
```
Linux/MacOS
```bash
.\install_dependencies.sh
```

Save installed packages:
```bash
pip freeze > requirements.txt 
```

## How to run test from terminal in VS Code
```bash
python .\[cesta]\tests.py
```