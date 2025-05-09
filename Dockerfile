FROM python:3.14-rc-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 53/udp 53/tcp

CMD ["python", "."]