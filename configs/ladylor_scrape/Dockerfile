FROM alpine:latest

RUN apk add --no-cache python3 py3-pip py3-requests

COPY scraper.py /app/scraper.py

RUN chmod +x /app/scraper.py

WORKDIR /app

CMD ["python3", "scraper.py"]