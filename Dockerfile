FROM python:3.9.5-alpine3.13

RUN mkdir -p /usr/share/dnshostupdater/bin
WORKDIR /usr/share/dnshostupdater/bin

COPY ddnshostupdater.py /usr/share/dnshostupdater/bin

ENV PATH /usr/share/dnshostupdater/bin:$PATH

ENTRYPOINT ["python3", "/usr/share/dnshostupdater/bin/ddnshostupdater.py"]