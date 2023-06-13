FROM nginx:latest
COPY nginx.conf /etc/nginx/nginx.conf
COPY certificate/* /etc/nginx
