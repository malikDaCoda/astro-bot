FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip3 install discord python-dotenv bcrypt validators pycryptodom && \
    rm -rf /var/lib/apt/lists/*

RUN useradd mate

COPY app /app

WORKDIR /app

RUN chmod +x app.py && \
    chown -R mate:mate

USER mate

ENTRYPOINT ["/app/app.py"]
