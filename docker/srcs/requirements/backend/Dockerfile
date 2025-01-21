FROM debian:latest

RUN apt update && apt upgrade -y

RUN mkdir transcendence

RUN apt install python3 -y && apt install python3-pip -y

RUN rm /usr/lib/python*/EXTERNALLY-MANAGED

ENV ENVIRONMENT=production

COPY tools/requirements.txt transcendence/requirements.txt
COPY tools/requirements-dev.txt transcendence/requirements-dev.txt

COPY tools/.flake8 transcendence/.flake8

COPY tools/backend.sh /usr/local/bin/

RUN chmod +x /usr/local/bin/backend.sh

ENTRYPOINT ["/usr/local/bin/backend.sh"]

CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000" ]
# CMD [ "gunicorn", "--bind", "0.0.0.0:8000", "backend.wsgi" ]
