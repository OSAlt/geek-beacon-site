#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
set -o xtrace

# start celery worker process in background along with beat scheduler to run periodic tasks
celery multi start w1 -A geekbeacon -B -l info

python manage.py migrate
python manage.py runserver_plus 0.0.0.0:8000
