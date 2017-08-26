#!/usr/bin/env bash
set -e

/usr/local/bin/gunicorn backend.wsgi -w 3 -b 0.0.0.0:8000 --chdir=/app
