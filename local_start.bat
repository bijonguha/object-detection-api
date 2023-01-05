#!/usr/bin/bash
# export APP_ENV='local'
# export DB_USERNAME='postgres'
# export DB_PASSWORD='qwer1234'
# export DB_HOST='localhost'
# export DB_PORT='5432'
# export DB_NAME='linked'
# export FASTAPI_SIMPLE_SECURITY_DB_LOCATION='/Users/bijonguha/codes/label-ocr/security/sqlite.db'
# export FASTAPI_SIMPLE_SECURITY_SECRET='garylabelocr'

#python docker_pytest.py && echo 'Tests running'
uvicorn src.main:app --reload --reload-dir src
