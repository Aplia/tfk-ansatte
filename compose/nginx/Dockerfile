FROM nginx:latest

RUN apt-get update \
    && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*
RUN curl -sLo /usr/local/bin/ep https://github.com/kreuzwerker/envplate/releases/download/v0.0.8/ep-linux \
    && chmod +x /usr/local/bin/ep

COPY start-nginx.sh /
RUN chmod +x /start-nginx.sh
ADD nginx.conf /etc/nginx/nginx.conf

CMD ["/start-nginx.sh"]
