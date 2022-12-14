# booksy CORS proxy 
Provides a local REST API endpoint (domain/api/booksyreviews) to retrieve and display booksy reviews on your website circumnavigating their CORS policy

For most of these "production ready" examples your encpoint for retreiving the reviews will be:  
> localhost:5000/booksyreviews

However the package is set up so that in the case this is used/integrated with another flask app this application will be behind the root path "/borev_api" therefore your reviews will be found under
> localhost:5000/boorev_api/booksyreviews  

This is not what is going on in the `Quickstart production docker-compose example`, the reverse proxy takes care of of routing the /api path in that situation (mechanics of reverse proxy routing can be seen under sample/ex-conf/httpd-vhosts.conf).  More information about dispatching under different root path:  https://flask.palletsprojects.com/en/2.1.x/patterns/appdispatch/#dispatch-by-path

---
## Install package
- #### From source:
    ```bash
    git clone https://github.com/RT-Tap/booksyCORSproxy
    pip install -e booksyAPI
    ```
- #### From source and Create Redistributable Package:
    ```bash
    git clone https://github.com/RT-Tap/booksyCORSproxy
    cd booksyAPI
    python setup.py bdist_wheel
    pip install dist/booksyAPI-1.0-py3-none-any.whl
    ```
- #### From download release/package: 
    - Get latest release from: https://github.com/RT-Tap/booksyCORSproxy/releases
    ```bash
    pip install booksyAPI-1.0-py3-none-any.whl
    ```  

---

## Environment Variables
### production / mandatory
- BOOKSYAPI_BUSREF:  The 6 digit ID of the business you want reviews for, See "Booksy Business Refrence/ID Number" section below
- BOOKSYAPI_PROXY: True/False - Will this be behind a reverse proxy?
- SERVER_NAME:  URL endpoint of website you intend to use this on eg. "booksyAPItest.com" - used to set our own CORS policy during production
- SECRET_KEY: used for encryption NEEDS to be changed to a random 24 byte string - can use following command to generate a random key : python -c 'import secrets; print(secrets.token_hex())'

### development / optional
- ROOT_PATH: default=boorev_api - Unless you are integrating with another flask app you dont need to worry about this
- FLASK_DEBUG: True/False - If you are in development True, production False - IMPORTANT! Used to set our own CORS policy
- booksyAPI_DEBUGSERVER: Flask/Waitress (optional, defaults: development=Flask production=waitress)
- DEBUG_LOCALONLY: True/Flase - when set to true will ONLY retrieve local example reviews (located in sample/samplereviews.txt ) usefull if you plan on working in a live environment constantly reloading/refreshing and therefore repeatedly requesting the same data from booksy but don't want to hit their request limits/raise suspicion
- FLASK_APP: booksyAPI - will most likely never change, used to let know server what application to run

#### How/Where do I set environment variables?
>|  Linux/iOS: |  Windows powershell: |   Windows cmd: |  (ana)conda: |  Docker: |
>|---|---|---|---|---|
>|```export name=val```|    ```$env:name=val``` | ``` set name=val``` | ```conda env config vars set NAME='val'``` | name=val |
>|  export FLASK_APP=booksyAPI |  $env:FLASK_ENV ="production" |  BOOKSYAPI_BUSREF=463431 |  conda env config vars set FLASK_APP='booksyAPI'|  booksyProxy.env  |


---
# Quickstart production docker-compose example 
### A sample/demo of how to use/integrate with website behind a reverse proxy
#### Creates a local website booksyAPItest.com behind a reverseProxy that displays the reviews it retrieves from booksyAPItest.com/api/booksyreviews

> 1. Set/Create DNS record to resolve domain (sample default=booksyAPItest.com) to the IP of the machine you are running this on 
>    - Windows: https://docs.microsoft.com/en-us/windows-server/networking/technologies/ipam/add-a-dns-resource-record  
>
>    - Linux/iOS: modify '/etc/hosts' to include '127.0.0.1    booksyAPItest.com'  
>
>    - Pi-Hole: https://discourse.pi-hole.net/t/documentation-on-local-dns-records/33777
>2. Change environment variables in sample/booksyProxy.env to liking
>3.  
>    ```
>    cd samples
>    docker-compose up -d 
>    ```
>4. > booksyAPItest.com  

### **NOTE:** you must create/get your own ssl cert and use it in the reverse proxy container. This sample uses a signed ssl cert that is publicly available and not for your domain 

---

# Production
Exposes following endpoint where you can GET reviews
> localhost:5000/booksyreviews
- ## Docker run
    1. Build image (choose one)
        - remotely
            - ```
                docker build https://github.com/RT-Tap/booksyCORSproxy.git#main -t booksyproxy/mydomain:1.0  
                ```  
        - Locally
            - ```  
                docker build . -t booksyproxy/mydomain:1.0  
                ```  
    
    2. Run image    
        - Remember: set the appropriate env vars in `docker run` command
        ```
        docker run -d -e BOOKSYAPI_BUSREF=123456 -e BOOKSYAPI_PROXY=False -e SERVER_NAME=booksyAPItest.com -e SECRET_KEY=123456789CHANGETHIS -p 5000:5000 booksyproxy/mydomain:1.0
        ```


- ## docker-compose
        git clone https://github.com/RT-Tap/booksyCORSproxy

    Set environment variables in sample/booksyProxy.env

        cd sample 
        docker-compose up -d  

- ## Module
    1. set mandatory env vars 
    2. install package
        ```
        pip install -e booksyAPI
        ```
    3. start server
        ```
        waitress-serve --port=5000 booksyAPI:app 
        ```
- ## Wheel package
    1. set mandatory env vars 
    1. create wheel package
        ```
        cd booksyAPI
        python setup.py bdist_wheel
        ```
    3. install wheel package
        ```
        pip install dist/booksyAPI-1.0-py3-none-any.whl
        ```
    3. Start Server
        ```
        waitress-serve --port=5000 booksyAPI:app
        ```

---
# Development
1. set (enviornment) variables
2. ``` 
    pip install -e booksyAPI
    ```
3. run the pacakge/module
    - Using Flask (any of the following will work)
        - ```
            flask --app booksyAPI run 
            ```
            - as long as you don't have another flask application running you can set environment variable FLASK_APP=booksyAPI and following will work    
        - ```
            flask run 
            ```
        - ```
            python bookyAPI/booksyAPI/views.py
            ```
    - Using Waitress (any of the following will work)
        - ```
            waitress-serve --port=5000 booksyAPI:app 
            ```  
            - set env var booksyAPI_DEBUGSERVER=Waitress
        - ```
            python bookyAPI/booksyAPI/views.py
            ```
4. > 127.0.0.1:5000/api/booksyreviews

---

## Booksy Business Refrence/ID Number 
1. Navigate to business on booksy.com
2. Open chrome/firefox inspector (right click >> Inspect)
    1. Go to Network tab
    2. Find entry "?reviews_page=1&reviews_per_page=20" 
        - Yellow box in following refrernce pic
    3. Get 6 digit refrence from request URL: 
        - Request URL will be something like: https://us.booksy.com/api/us/2/customer_api/businesses/123456/reviews/?reviews_page=1&reviews_per_page=20
        - the "123456" from above is what you want
        - Red box inside blue box of following refrence picture

![Refrence Picture](https://github.com/RT-Tap/booksyCORSproxy/raw/main/sample/ex-site/booksy-business-pic.png "Refrence Picture to what your looking for")


---

## Future 
- Allow other integrattions such as gunicorn or mod_wsgi for production and/or development
- create a (polling) cache so that a request  isn't made for every visitor 
