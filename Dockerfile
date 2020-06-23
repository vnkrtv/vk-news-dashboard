FROM python:3.7
MAINTAINER LeadNess

RUN python3.7 -m venv /usr/share/python3/venv
RUN /usr/share/python3/venv/bin/pip install -U pip

COPY requirements.txt /mnt/
RUN apt-get install -y libpq-dev \
 && /usr/share/python3/venv/bin/pip install -Ur /mnt/requirements.txt

COPY . /usr/share/python3/vk-news-dashboard
COPY deploy/entrypoint /entrypoint

RUN chmod +x /entrypoint
ENV TZ=Europe/Moscow

ENTRYPOINT ["/entrypoint"]
