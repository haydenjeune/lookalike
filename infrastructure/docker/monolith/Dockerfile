# Build the production UI distribution
FROM node:16.9-alpine as ui_build
COPY ./web/lookalike-web /workdir
WORKDIR /workdir
RUN npm run build


FROM curlimages/curl:7.79.1 as model_artifact
WORKDIR /data
RUN curl https://github.com/timesler/facenet-pytorch/releases/download/v2.2.9/20180402-114759-vggface2.pt -LO --output-dir /data


FROM python:3.8.12-slim
LABEL org.opencontainers.image.source https://github.com/haydenjeune/lookalike-demo

# Install API
COPY ./dist/src.api /api

# Copy downloaded model artifact into the image
COPY --from=model_artifact /data /api/.model/checkpoints
ENV TORCH_HOME="/api/.model"

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

RUN useradd -mr supervisor
USER supervisor

CMD ["supervisord", "-n", "-c", "/etc/supervisord.conf"]
