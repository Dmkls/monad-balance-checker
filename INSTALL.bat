@echo off

IF EXIST ".\.venv" (
	call .\.venv\Scripts\activate
) ELSE (
	echo creating env..
	python -m venv .venv
)

IF NOT EXIST ".\data" (
	mkdir "data"
)

pip install -r requirements.txt
pause