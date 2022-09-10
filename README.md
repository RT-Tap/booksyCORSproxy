# booksy CORS proxy 
## Provides a local REST API endpoint (domain/api/booksyreviews) to retrieve and display booksy reviews on your website circumnavigating their CORS policy

### Install package
    - From source:
        - pip install -e booksyAPI
    - From source, using distributable:
        - cd booksyAPI
        - python setup.py bdist_wheel
        - pip install dist/booksyAPI-1.0-py3-none-any.whl
    - Download: 
        - Download wheel file (.whl ) from releases section of this repo 
        - pip install booksyAPI-1.0-py3-none-any.whl

### Environment Variables
(production mandatory)
    - BOOKSYAPI_BUSREF:  The 6 digit ID of the business you want reviews for, See "Booksy Business Refrence/ID Number" section below
    - BOOKSYAPI_PROXY: True/False - Will this be behind a reverse proxy?
    - SERVER_NAME:  URL endpoint of website you intend to use this on eg. "booksyAPItest.com" - used to set our own CORS policy during production
    - SECRET_KEY: used for encryption NEEDS to be changed to a random 24 byte string - can use following command to generate a random key : python -c 'import secrets; print(secrets.token_hex())'
(development optional)
    - FLASK_APP: booksyAPI
    - FLASK_DEBUG: True/False - If you are in development True, production False - IMPORTANT! Used to set our own CORS policy
    - booksyAPI_DEBUGSERVER: Flask/Waitress (optional, defaults: development=Flask production=waitress)
    - DEBUG_LOCALONLY: True/Flase - when set to true will ONLY retrieve local example reviews (located in sample/samplereviews.txt ) usefull if you plan on working in a live environment constantly reloading/refreshing and therefore repeatedly requesting the same data from booksy but don't want to hit their request limits/raise suspicion
### How Do i set environment variables?
    - Linux/iOS: export FLASK_APP=booksyAPI  
    - Windows powershell: $env:FLASK_ENV ="production"
    - Windows cmd: set BOOKSYAPI_BUSREF=463431
    - (ana)conda: conda env config vars set FLASK_APP='booksyAPI:app'
    - Docker: samples/Dockerfile
    - docker-compose: samples/booksyProxy.env or using environment section of .yml

## Quickstart production docker-compose sample 
### A sample/demo of how to use/integrate with website behind a reverse proxy
#### Creates a local website booksyAPItest.com behind a reverseProxy that displays the reviews it retrieves from booksyAPItest.com/api/booksyreviews
1. Set/Create DNS record to resolve domain (sample default=booksyAPItest.com) to the IP of the machine you are running this on :
    - Windows: https://docs.microsoft.com/en-us/windows-server/networking/technologies/ipam/add-a-dns-resource-record
    - Linux/iOS: modify '/etc/hosts' to include '127.0.0.1    booksyAPItest.com'
    - Pi-Hole: https://discourse.pi-hole.net/t/documentation-on-local-dns-records/33777
3. Change environment variables in sample/booksyProxy.env to liking
4. docker-compose up -d 
5. booksyAPItest.com available in browser

## Development
1. set (enviornment) variables
2. pip install -e booksyAPI
3. run the pacakge/module
    - Using Flask
        - flask --app booksyAPI run 
        - flask run - if you don't have another flask application running you can set the environment variable FLASK_APP to booksyAPI and simply use 'flask run'
        - python bookyAPI/booksyAPI/views.py
    - Using Waitress
        - waitress-serve --port=5000 booksyAPI:app
        - python bookyAPI/booksyAPI/views.py ( set env var booksyAPI_DEBUGSERVER=Waitress )
4. Endpoint available @ 127.0.0.1:5000/api/booksyreviews

## Qucikstart Production
## Docker
### Container
    - docker build https://github.com/docker/thisrepo.git#container:sample -t booksyAPI/mydomain:1.0
    - docker run -d -e BOOKSYAPI_BUSREF=123456 -e BOOKSYAPI_PROXY=False -e SERVER_NAME=booksyAPItest.com -e SECRET_KEY=123456789CHANGETHIS -p 5000:5000 booksyAPI/mydomain:1.0
### docker-compose
    - clone sample/Dockerfile & sample/docker-compose.yml
    - set mandatory env vars in booksyProxy.env or individually in environment section of docker-compose.yml
    - docker-compose up -d
## As module
    - set mandatory env vars (see "How Do i set environment variables?" section)
    - waitress-serve --port=5000 booksyAPI:app


# Booksy Business Refrence/ID Number 
1. Navigate to business on booksy.com
2. Open chrome/firefox inspector (right click >> Inspect)
    1. Go to Network tab
    2. Find entry "?reviews_page=1&reviews_per_page=20" 
        - Yellow box in following refrernce pic
    3. Get 6 digit refrence from request URL: 
        - Request URL will be something like: https://us.booksy.com/api/us/2/customer_api/businesses/123456/reviews/?reviews_page=1&reviews_per_page=20
        - the "123456" from above is what you want
        - Red box inside blue box of following refrence picture
![Refrence Picture](https://github.com/blah/booksy-business-pic.png "Refrence Picture to what your looking for")

### Future plans (if there is demand)
Allow other integrattions such as gunicorn or mod_wsgi for production and/or development
create a (polling) cache so that a request  isn't made for every visitor 
