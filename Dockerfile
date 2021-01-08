### BASE
FROM python:3.8-slim-buster AS base

EXPOSE 5000

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y vim libpq-dev \
    build-essential libssl-dev libffi-dev \
    python3-setuptools python3-pip
#    sudo apt-get install libpcre3 libpcre3-dev
# python3-setuptools python3-pip python3-dev

# Install pip requirements
ADD requirements.txt .

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

CMD ["uwsgi", "--ini", "uwsgi.ini"]
