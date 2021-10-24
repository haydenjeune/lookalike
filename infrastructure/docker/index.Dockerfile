FROM python:3.8.12-slim

COPY ./dist/src.index /app
COPY ./dist/index_files /index
ENV INDEX_ROOT=/index

RUN groupadd app && \
    useradd -m -g app app
RUN chown app /app && \
    chmod +r /index
USER app
WORKDIR /app

CMD ["./index.pex"]
