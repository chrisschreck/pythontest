FROM ubuntu:latest
LABEL authors="cschreck"

ENTRYPOINT ["top", "-b"]