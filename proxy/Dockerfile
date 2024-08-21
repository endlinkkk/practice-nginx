FROM nginx:alpine

RUN apk add --no-cache python3 py3-pip clamav clamav-daemon
RUN pip3 install requests

COPY nginx.conf /etc/nginx/nginx.conf
COPY proxy_handler.py /app/proxy_handler.py

CMD ["sh", "-c", "nginx && python3 /app/proxy_handler.py"]