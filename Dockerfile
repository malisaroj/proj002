FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /startupql
WORKDIR /startupql
COPY requirements.txt /startupql/
RUN pip install -r requirements.txt
COPY . /startupql/