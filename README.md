venv environment

prefect version:

Version:             2.19.4
API version:         0.8.4
Python version:      3.12.3
Git commit:          867543a8
Built:               Tue, Jun 4, 2024 3:14 PM
OS/Arch:             win32/AMD64
Profile:             default
Server type:         ephemeral
Server:
  Database:          sqlite
  SQLite version:    3.45.1

pip install -U "prefect==2.19.4"

pip install yr_weather

python -m venv prefect-env          //create venv environment

\prefect-env\Scripts\activate.ps1   //activate venv environment

prefect version

prefect server start