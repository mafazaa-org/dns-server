FROM python:3.14-rc-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt


# install essential dnsutils tools
RUN apt-get update && apt-get install -y --no-install-recommends dnsutils && \
rm -rf /var/lib/apt/lists/*

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
CMD nslookup -type=A example.com 127.0.0.1 >/dev/null 2>&1 || exit 1

EXPOSE 53/udp 53/tcp

ENTRYPOINT ["python", "."]
