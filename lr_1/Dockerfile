FROM alpine:3.11

WORKDIR /app
RUN apk add python3
ADD simple_python_script ./

ENTRYPOINT [ "python3", "/app" ]
