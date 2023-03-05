# Production Stage
FROM nginx:stable-alpine as production-stage

RUN apk add --no-cache python3 py3-pip

ENV PYTHONUNBUFFERED 1

ENV SERVER_HOME=/usr/share/nginx/html

WORKDIR $SERVER_HOME

RUN set -e; \
        apk add --no-cache --virtual .build-deps \
                gcc \
                libc-dev \
                linux-headers \
                mariadb-dev \
                python3-dev \
                postgresql-dev \
        ;

COPY ./requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY ./server/nginx.conf /etc/nginx/conf.d/default.conf

COPY ./server/start.sh $SERVER_HOME/start.sh

RUN chmod 777 $SERVER_HOME/start.sh

RUN chown nginx:nginx $SERVER_HOME

ENTRYPOINT ["/bin/sh", "./start.sh"]

EXPOSE 80