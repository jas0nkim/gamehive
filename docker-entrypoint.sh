#!/bin/bash

ENTRYPOINT="$*"

if [ -z "$ENTRYPOINT" ]; then
    gunicorn --bind 0.0.0.0:5000 --workers 4 --chdir /src app:app
else
    /bin/sh -c "$ENTRYPOINT"
fi
