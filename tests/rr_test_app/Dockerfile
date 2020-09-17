FROM golang:latest

RUN apt-get update && apt-get install -y wget && apt-get install -y openssh-client git build-essential libsqlite3-dev sqlite3 bzip2 libbz2-dev zlib1g-dev libssl-dev openssl libgdbm-dev libgdbm-compat-dev liblzma-dev libreadline-dev libncursesw5-dev libffi-dev uuid-dev chrpath && apt-get clean

RUN wget https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tgz && tar xzf Python-3.7.2.tgz
RUN cd Python-3.7.2 && ./configure --enable-optimizations --enable-shared LDFLAGS="-Wl,-rpath /usr/local/lib" && make install

WORKDIR /app
RUN mkdir /app/pygoridge
COPY pygoridge ./pygoridge
COPY tests/rr_test_app/ .

RUN go mod download
RUN go build -a -ldflags="-s" -o /app/server /app/server.go

CMD ["/app/server"]