FROM python:alpine3.10
ENV PYTHONUNBUFFERED=1
WORKDIR /code

COPY ./requirements.txt ./

RUN apk update \
    && apk add libpq postgresql-dev \
    && apk add build-base

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY ./src ./src
EXPOSE 8000
# CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
