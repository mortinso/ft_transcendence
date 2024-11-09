FROM debian:latest

RUN apt update && apt upgrade -y

RUN apt install -y postgresql && apt install -y systemctl

COPY tools/postgresql.sh /usr/local/bin/

RUN chmod +x /usr/local/bin/postgresql.sh

# ENTRYPOINT ["/usr/local/bin/postgresql.sh"]

CMD [ "tail", "-f" ]
