FROM alpine:3.11

WORKDIR /app
RUN apk add python3
ADD script.py ./

ENTRYPOINT [ "python3", "/app/script.py" ]
