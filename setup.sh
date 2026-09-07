openssl req -x509 -newkey rsa:4096 -keyout nginx/private.key -out nginx/cert.pem -days 365 -sha256 -nodes -subj "/C=US"
openssl genrsa -out auth/private.key 2048
openssl rsa -in auth/private.key -pubout -out public.key