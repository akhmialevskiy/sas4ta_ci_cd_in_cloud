FROM python:3.9-slim-buster

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential libpq-dev telnet netcat \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app
ENV PYTHONPATH "${PYTHONPATH}:."

COPY ./requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt

ADD ./src/libs /app/libs
COPY ./src/services/trends_aggregator /app/services/trends_aggregator

CMD ["uvicorn", "services.trends_aggregator.main:app", "--host 0.0.0.0"]