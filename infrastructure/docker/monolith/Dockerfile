# Build the production UI distribution
FROM node:16.9-alpine as ui_build
COPY ./web/lookalike-web /workdir
WORKDIR /workdir
RUN npm run build


FROM python:3.8-slim
LABEL org.opencontainers.image.source https://github.com/haydenjeune/lookalike

# Install API
COPY ./dist/src.api /api

# Install Index
COPY ./dist/src.index /index
COPY ./dist/index_files /index/files
ENV INDEX_ROOT=/index/files

# Install UI
COPY --from=ui_build /workdir/build /ui

# Copy static images
# Expected to refect the naming conventions and structure of the worker output folder.
ARG IMAGE_ROOT="./.data"
COPY ${IMAGE_ROOT} /images

# Setup supervisord
RUN pip install supervisor
COPY ./infrastructure/docker/monolith/supervisord.conf /etc/supervisord.conf

CMD ["supervisord", "-n", "-c", "/etc/supervisord.conf"]
