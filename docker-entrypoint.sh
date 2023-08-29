#!/bin/sh
set -e
set -u

export $(cat /etc/custom/drivers | xargs)

if [ -n "${MODE}" ] && [ "${MODE}" != "dev" ]; then
  uwsgi --http "0.0.0.0:5000" --master -b 32768 -w wsgi:app
else
  flask run
fi
