FROM debian:latest

RUN apt update

RUN apt upgrade -y

RUN mkdir transcendence

RUN apt install python3 -y

RUN apt update

RUN apt install python3-pip -y

RUN rm /usr/lib/python*/EXTERNALLY-MANAGED

RUN apt install python3-venv -y

COPY conf/requirements.txt transcendence/requirements.txt

COPY tools/backend.sh /usr/local/bin/

RUN chmod +x /usr/local/bin/backend.sh

ENTRYPOINT ["/usr/local/bin/backend.sh"]

CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000" ]
# CMD [ "tail", "-f" ]
