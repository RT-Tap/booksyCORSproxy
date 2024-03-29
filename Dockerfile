FROM python:3.10-alpine3.15
RUN apk update && apk add python3-dev gcc libc-dev build-base
WORKDIR /usr/src/app
COPY ./booksyAPI ./booksyCORSproxy
RUN pip install -e booksyCORSproxy
ENV FLASK_APP="booksyCORSproxy"
#!!! YOU MUST CHANGE SECRET_KEY !!!!!
ARG SECRET_KEY="CHANGEMEPLZ"
ENV SECRET_KEY=$SECRET_KEY
EXPOSE 5000
CMD ["python", "-m", "booksyCORSproxy"]