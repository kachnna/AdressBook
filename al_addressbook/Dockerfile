FROM python:3.11-alpine

ENV APP_HOME /app

RUN pip install pipenv

WORKDIR /app

COPY Pipfile Pipfile.lock /app/

RUN pipenv install --deploy --system

COPY . /app/

CMD ["python", "book/main.py"]