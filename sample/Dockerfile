FROM python:3.10-alpine3.15
# follwoing RUN apk is needed to build wheel files due to errors, fixes refrence :
# https://stackoverflow.com/questions/60595581/failed-to-install-gcc-on-python-3-7-alpine-docker-container
# https://stackoverflow.com/questions/11912878/gcc-error-gcc-error-trying-to-exec-cc1-execvp-no-such-file-or-directory
RUN apk update && apk add python3-dev gcc libc-dev build-base
WORKDIR /usr/src/app
# COPY ../booksyAPI/dist/booksyAPI-1.0-py3-none-any.whl .
# RUN pip install ./booksyAPI-1.0-py3-none-any.whl
COPY booksyAPI .
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