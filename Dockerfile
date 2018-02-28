FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir -p /code
WORKDIR /code
COPY requirements.txt /code/
COPY requirements.dev.txt /code/
RUN pip install -U pip
RUN pip install -r requirements.txt -r requirements.dev.txt
COPY . /code/
