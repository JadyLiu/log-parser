FROM python:slim-buster

EXPOSE 8080
COPY web/index.html .

ENTRYPOINT [ "python3", "-m", "http.server", "8080" ]