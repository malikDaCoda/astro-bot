FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN useradd astro

COPY app /app/

COPY run.sh /

WORKDIR /app

RUN python3 -m pip install -r requirements.txt && \
    chmod +x app.py /run.sh && \
    chown -R astro:astro .

USER astro

ENTRYPOINT ["/run.sh"]
