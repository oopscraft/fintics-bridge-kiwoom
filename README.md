# fintics-bridge-kiwoom
Fintics bridge kiwoom

## Install python(32bit)
https://www.python.org/downloads/windows/

## pip uptrade
```powershell
python -m pip install --upgrade pip
```

## Project install
```powershell
python -m venv .venv
# 현재 사용자에 대한 스크립트 실행 허용
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
.\.venv\Scripts\activate
pip install -r requirements.txt
```

## Run application
```shell
# powershell
$env:PYTHONPATH="$env:PYTHONPATH;."

# run
python fintics_bridge_kiwoom/app.py

```