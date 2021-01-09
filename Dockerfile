### BASE
FROM python:3.8-slim-buster AS base

EXPOSE 5000

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y vim libpq-dev \
    build-essential libssl-dev libffi-dev \
    python3-dev python3-setuptools python3-pip

# Install pip requirements
ADD requirements.txt .

RUN python -m pip install --upgrade pip

WORKDIR /app
ADD . /app



### DEV
FROM base AS development

ADD requirements-dev.txt .
RUN python -m pip install -r requirements-dev.txt

CMD ["flask", "run", "--reload", "--debugger", "--host", "0.0.0.0"]


### PROD
FROM base AS production

ADD requirements-prod.txt .
RUN python -m pip install -r requirements-prod.txt

# Switching to a non-root user, please refer to https://aka.ms/vscode-docker-python-user-rights
RUN useradd appuser && chown -R appuser /app
USER appuser

# it works without nginx
# CMD ["uwsgi", "--socket", "0.0.0.0:5000", "--protocol=http", "-w", "wsgi:app"]

# Another way without ini file
# CMD ["uwsgi", "--wsgi-file", "wsgi.py", "--socket", "0.0.0.0:5000", "--wsgi-disable-file-wrapper", "--threads", "4"]

CMD ["uwsgi", "--ini", "uwsgi.ini"]
