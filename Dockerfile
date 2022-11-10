FROM python:3.10

WORKDIR /app
RUN apt-get update -y
RUN apt-get install build-essential
RUN pip install poetry


COPY poetry.lock pyproject.toml .python-version /app/

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

COPY . /app

# docker build . -t business-financial-orquestrator
# docker run -it business-financial-orquestrator     /bin/bash