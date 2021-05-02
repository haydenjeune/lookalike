FROM python:3.8-slim

COPY ./dist/src.api /app
COPY .celebstore/vec /vec

RUN groupadd app && \
    useradd -m -g app app
RUN chown app /app && \
    chmod +r /vec
USER app
WORKDIR /app

ENV VECTOR_INDEX_FILEPATH /vec

# TODO: actually run this with gunicorn rather than dev server
CMD ["./api.pex"]
