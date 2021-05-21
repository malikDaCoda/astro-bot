FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    python3 -m pip install -r requirements.txt && \
    rm -rf /var/lib/apt/lists/*

RUN useradd mate

COPY app /app

WORKDIR /app

RUN chmod +x app.py && \
    chown -R mate:mate

USER mate

ENTRYPOINT ["/app/app.py"]
