#!/usr/bin/env bash

set -e

PROJECT_PATH='/usr/local/apps'

git pull
$PROJECT_PATH/env/bin/python3 -m pip install -r $PROJECT_PATH/requirements.txt
$PROJECT_PATH/env/bin/python3 manage.py migrate
$PROJECT_PATH/env/bin/python3 manage.py collectstatic --noinput
supervisorctl restart profiles_api

echo "DONE! :)"
