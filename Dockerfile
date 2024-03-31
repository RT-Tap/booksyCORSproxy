FROM python:3.10-alpine
RUN apk update && apk add python3-dev gcc libc-dev build-base
#COPY ./booksyAPI ./booksyCORSproxy
COPY ./booksyAPI /usr/booksyCORSproxy_tmp
RUN chmod -R 777 /usr/src && chmod -R 777 /usr/booksyCORSproxy_tmp && mv /usr/booksyCORSproxy_tmp /usr/src/app/booksyCORSproxy 
WORKDIR /usr/src/app
RUN pip install -e booksyCORSproxy
#RUN whoami && ls -la /usr/src && chmod -R 777 /usr/src && pip install -e booksyCORSproxy
#RUN chmod -R 777 /usr/src && pip install -e booksyCORSproxy
#RUN chmod -R 777 /usr/src				# docker in namespace isoation throwing errors when trying to build
#RUN pip install -e booksyCORSproxy
ENV FLASK_APP="booksyCORSproxy"
#!!! YOU MUST CHANGE SECRET_KEY !!!!!
ARG SECRET_KEY="CHANGEMEPLZ"
ENV SECRET_KEY=$SECRET_KEY
EXPOSE 5000
CMD ["python", "-m", "booksyCORSproxy"]
