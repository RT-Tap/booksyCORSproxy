FROM python:3.10-alpine3.15
RUN apk update && apk add python3-dev gcc libc-dev build-base
WORKDIR /usr/src/app
COPY ./booksyAPI .
RUN pip install -e booksyAPI
ENV FLASK_APP="booksyAPI"
ENV FLASK_DEBUG="False"
ENV BOOKSYAPI_BUSREF="463431"
ENV BOOKSYAPI_PROXY="True"
ENV SERVER_NAME="booksyAPItest.com"
# Following NEEDS to be changed - use: python -c 'import secrets; print(secrets.token_hex())'
ENV SECRET_KEY="CHANGEME"  
EXPOSE 5000
CMD ["waitress-serve", "--port=5000", "booksyAPI:app"]