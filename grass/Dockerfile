FROM python:3.7

ENV PYTHONUNBUFFERED=1

RUN mkdir /grass
RUN mkdir /grass/src

WORKDIR /grass

COPY ./requirements ./requirements
RUN pip install --disable-pip-version-check --no-cache-dir -r ./requirements/base.txt

COPY ./src /grass/src
COPY ./wait-for-it.sh /grass/wait-for-it.sh
COPY ./start.sh /grass/start.sh

WORKDIR /grass/src

ENTRYPOINT ["bash", "../wait-for-it.sh", "rabbit:5672", "-t", "60", "--", "sh", "../start.sh"]
