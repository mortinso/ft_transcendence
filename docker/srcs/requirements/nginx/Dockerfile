FROM nginx:1.27.3

RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/nginx-selfsigned.key -out /etc/ssl/certs/nginx-selfsigned.crt -subj "/C=PT/ST=Lx/L=Lx/O=42/OU=42/CN=anda-cun.42.fr/UID=anda-cun"

# COPY conf/default.conf /etc/nginx/conf.d

CMD [ "nginx", "-g", "daemon off;" ]
