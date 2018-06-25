FROM ubuntu:16.04
RUN apt-get update -y && \
    apt-get install -y python-pip && \
    pip install flask uwsgi && \
    rm -rf /var/lib/apt/lists/*
COPY . /app
WORKDIR /app
ENTRYPOINT ["uwsgi"]
CMD ["--http", "0.0.0.0:8080", "--master", "--module", "base.base", "--processes", "1"]
EXPOSE 8080