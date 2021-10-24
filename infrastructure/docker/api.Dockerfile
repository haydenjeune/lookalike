FROM python:3.8.12-slim

COPY ./dist/src.api /app

RUN groupadd app && \
    useradd -m -g app app
RUN chown app /app
USER app
WORKDIR /app

# TODO: actually run this with gunicorn rather than dev server
CMD ["./api.pex"]
