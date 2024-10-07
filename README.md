# fintics-bridge-kiwoom
Fintics bridge kiwoom

**(버그 쩔고 해외증권은 안되서 중단함. 배부른 키움증권...)**

## Install OCX
관리자모드로 cmd 창에서 COM 등록
```shell
regsvr32 C:/OpenAPI/khopenapi.ocx
```

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