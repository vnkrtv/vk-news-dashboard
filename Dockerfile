FROM snakepacker/python:all as builder
MAINTAINER LeadNess

RUN python3.7 -m venv /usr/share/python3/venv
RUN /usr/share/python3/venv/bin/pip install -U pip

COPY requirements.txt /mnt/
RUN /usr/share/python3/venv/bin/pip install -Ur /mnt/requirements.txt

FROM snakepacker/python:3.7 as api

COPY --from=builder /usr/share/python3/venv /usr/share/python3/venv
COPY . /usr/share/python3/vk-news-dashboard
COPY deploy/entrypoint /entrypoint

ENTRYPOINT ["/entrypoint"]