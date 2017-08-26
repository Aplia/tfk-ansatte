#!/usr/bin/env bash
set -e
cmd="$@"

# This entrypoint is used to play nicely with the current cookiecutter configuration.
# Since docker-compose relies heavily on environment variables itself for configuration, we'd have to define multiple
# environment variables just to support cookiecutter out of the box. That makes no sense, so this little entrypoint
# does all this for us.

function postgres_ready(){
     python << END
import sys
import psycopg2
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
try:
    db = settings.DATABASES['default']
    conn = psycopg2.connect(dbname=db["NAME"], user=db["USER"], password=db["PASSWORD"], host=db["HOST"], port=db["PORT"])
except (psycopg2.OperationalError, ImproperlyConfigured) as e:
    print(e)
    sys.exit(-1)
sys.exit(0)
END
}

if [ -z $DATABASE_SKIP ]; then
    if [ -n $DATABASE_WAIT ]; then
        until postgres_ready; do
          >&2 echo "Postgres is unavailable - sleeping"
          sleep 1
        done

        >&2 echo "Postgres is up - continuing..."
    fi
fi

exec $cmd
