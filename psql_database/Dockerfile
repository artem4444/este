FROM postgres:17.2

ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=Mozart90-
ENV POSTGRES_DB=mas_tables

COPY ./init.sql /docker-entrypoint-initdb.d/init.sql
#init.sql musst be by same path as this Dockerfile