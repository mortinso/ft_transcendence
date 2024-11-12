FROM debian:latest

RUN apt update && apt upgrade -y

RUN mkdir transcendence

RUN apt install python3 -y && apt install python3-pip -y

RUN rm /usr/lib/python*/EXTERNALLY-MANAGED

COPY tools/requirements.txt transcendence/requirements.txt

COPY tools/backend.sh /usr/local/bin/

# RUN mkdir temp temp/backend temp/users temp/auth

# COPY conf/backend/* /temp/backend

# COPY conf/users/* /temp/users

# COPY conf/auth/* /temp/auth

RUN chmod +x /usr/local/bin/backend.sh

ENTRYPOINT ["/usr/local/bin/backend.sh"]

CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000" ]
# CMD [ "tail", "-f" ]
