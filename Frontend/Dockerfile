FROM nginx:stable-alpine

COPY auth.html /usr/share/nginx/html/
COPY dashboard.html /usr/share/nginx/html/

RUN echo "server { \
    listen 80; \
    root /usr/share/nginx/html; \
    index auth.html; \
    location / { \
        try_files \$uri \$uri/ /auth.html; \
    } \
}" > /etc/nginx/conf.d/default.conf