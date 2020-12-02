FROM python:3

# Set env variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y netcat

# Install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

COPY . /usr/src/app/

RUN chmod +x /usr/src/app/entrypoint.sh
