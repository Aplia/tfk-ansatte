#!/usr/bin/env bash
# How many to seconds to wait before retrying
ERROR_RETRY_DELAY=${ERROR_RETRY_DELAY-5}

# Run migrations, retry on failure
while true; do
    python manage.py migrate
    if [ $? -eq 0 ]; then
        break
    else
        echo "Django migration failed, sleeping $ERROR_RETRY_DELAY seconds and retrying"
        sleep $ERROR_RETRY_DELAY
    fi
done

# Start server, retry on failure
while true; do
    if [ "${DJANGO_RUNSERVER-default}" = "plus" ]; then
        python manage.py runserver_plus 0.0.0.0:8000
    else
        python manage.py runserver 0.0.0.0:8000
    fi
    if [ $? -eq 0 ]; then
        break
    else
        echo "Django application failed, sleeping $ERROR_RETRY_DELAY seconds and retrying"
        sleep $ERROR_RETRY_DELAY
    fi
done
