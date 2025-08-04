test otestuje přihlášení uživatele "standard\_user"
potom otestuje přidání zboží do košíku a jeho odebrání a to pro čtyři druhy zboží
logování probíhá do souboru my\_log.log
při spuštění pomocí "pytest --html=report.html" navíc vytvoří log test v html

do venv přidán pytest-html

conftest.py přidán kvůli možnosti logování do my\_log.log při testování pomocí pytest,
v setup\_8.py je nastavení logování pouze mimo pytest (konstrukce AI)

