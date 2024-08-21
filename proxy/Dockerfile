FROM alpine:latest

RUN apk add --no-cache python3 py3-pip clamav clamav-daemon
RUN pip install --break-system-packages requests uvicorn fastapi python-multipart

COPY proxy/proxy_handler.py /app/proxy_handler.py

CMD ["sh", "-c", "python3 /app/proxy_handler.py"]