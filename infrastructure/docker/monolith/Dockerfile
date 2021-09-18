FROM node:16.9-alpine as ui_build
COPY ./web/lookalike-web /workdir
WORKDIR /workdir
RUN npm run build

FROM python:3.8-slim

# install API
COPY ./dist/src.api /api

# install Index
COPY ./dist/src.index /index
COPY ./dist/index_files /index/files
ENV INDEX_ROOT=/index/files

# install UI
COPY --from=ui_build /workdir/build /ui

# setup supervisord
RUN pip install supervisor
COPY ./infrastructure/docker/monolith/supervisord.conf /etc/supervisord.conf

CMD ["supervisord", "-n", "-c", "/etc/supervisord.conf"]
