FROM python:3.5.4
ENV PYTHONUNBUFFERED 1

RUN groupadd -r django \
    && useradd -r -g django django

# Requirements have to be pulled and installed here, otherwise caching won't work
COPY ./backend/requirements /requirements
RUN pip install --no-cache-dir -r /requirements/prod.txt \
    && rm -rf /requirements

COPY ./compose/django/gunicorn.sh ./compose/django/entrypoint.sh /
RUN sed -i 's/\r//' /entrypoint.sh \
    && sed -i 's/\r//' /gunicorn.sh \
    && chmod +x /entrypoint.sh \
    && chown django /entrypoint.sh \
    && chmod +x /gunicorn.sh \
    && chown django /gunicorn.sh

COPY ./backend /app
RUN mkdir -p /app/staticfiles

RUN chown -R django /app
RUN rm -f /app/settings/local.py && \
    echo "# coding=utf-8\nfrom .prod import *  # noqa\n" > /app/settings/local.py
RUN rm -f /app/settings/.env && \
    echo "" > /app/settings/.env

USER django

WORKDIR /app

EXPOSE 8000
ENTRYPOINT ["/entrypoint.sh"]
CMD ["/gunicorn.sh"]
