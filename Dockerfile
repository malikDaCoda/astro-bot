FROM python:3.6

RUN useradd astro

COPY app /app/

COPY run.sh /

WORKDIR /app

RUN chmod +x app.py /run.sh && \
    chown -R astro:astro .

RUN python -m pip install -r requirements.txt

USER astro

ENTRYPOINT ["/run.sh"]
