#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
set -o xtrace


python manage.py migrate
python manage.py runserver_plus
