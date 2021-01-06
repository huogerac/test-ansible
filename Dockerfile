### PROD
FROM python:3.8-slim-buster AS production

EXPOSE 5000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y vim libpq-dev 

# Install pip requirements
ADD requirements.txt .

RUN python -m pip install -r requirements.txt

WORKDIR /app
ADD . /app

# Switching to a non-root user, please refer to https://aka.ms/vscode-docker-python-user-rights
RUN useradd appuser && chown -R appuser /app
USER appuser

CMD ["uwsgi", "--ini", "uwsgi.ini"]


### DEV
FROM production AS development

CMD ["flask", "run", "--reload", "--debugger", "--host", "0.0.0.0"]
