#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

# start celery worker process in background along with beat scheduler to run periodic tasks
celery multi start w1 -A geekbeacon -B -l info

python /app/manage.py collectstatic --noinput
/usr/local/bin/gunicorn geekbeacon.wsgi -w 4 -b 0.0.0.0:5000 --chdir=/app
