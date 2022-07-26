FROM python:3.9.1-buster

ARG SENTRY_SDK_VERSION=master
ENV SENTRY_SDK_VERSION=$SENTRY_SDK_VERSION

ARG SENTRY_PORT_BACKEND=8080
ENV SENTRY_PORT_BACKEND=$SENTRY_PORT_BACKEND

ARG APP_ENABLE_PROFILING=0
ENV APP_ENABLE_PROFILING=$APP_ENABLE_PROFILING

ARG SENTRY_DSN=""
ENV SENTRY_DSN=$SENTRY_DSN

WORKDIR /django

COPY requirements.txt ./
RUN pip install -r requirements.txt
RUN pip install git+https://github.com/getsentry/sentry-python.git@${SENTRY_SDK_VERSION}
COPY . ./

EXPOSE ${SENTRY_PORT_BACKEND}

CMD ["gunicorn", "--pid=gunicorn.pid", "hello.wsgi:application", "-c", "gunicorn_conf.py", "--env", "DJANGO_DB=postgresql", "--log-level", "debug"]
