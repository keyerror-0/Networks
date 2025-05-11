FROM python:3.12-alpine

RUN apk update && apk add --no-cache \
    gcc \
    musl-dev \
    postgresql-dev \
    postgresql-client \
    && rm -rf /var/cache/apk/*

RUN adduser -D appuser && \
    mkdir -p /project && \
    chown -R appuser:appuser /project

WORKDIR /project
USER appuser

COPY --chown=appuser:appuser requirements.txt .

ENV PATH="/home/appuser/.local/bin:${PATH}"
RUN pip install --user --no-cache-dir -r requirements.txt

COPY --chown=appuser:appuser . .

RUN chmod +x entrypoint.sh

EXPOSE 5000

ENTRYPOINT ["/project/entrypoint.sh"]
CMD ["flask", "run"]