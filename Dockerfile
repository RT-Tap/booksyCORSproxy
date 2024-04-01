FROM python:3.10-alpine
# git needed for temporary flask_api fix
RUN apk update && apk add python3-dev gcc libc-dev build-base git
WORKDIR /usr/src/app
COPY --chmod=777 ./booksyCORSproxy ./booksyCORSproxy
RUN pip install -e booksyCORSproxy
ENV FLASK_APP="booksyCORSproxy"
#!!! YOU MUST CHANGE SECRET_KEY !!!!!
ARG SECRET_KEY="CHANGEMEPLZ"
ENV SECRET_KEY=$SECRET_KEY
EXPOSE 5000
CMD ["python", "-m", "booksyCORSproxy"]
