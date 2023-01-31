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
- SECRET_KEY: used for encryption NEEDS to be changed to a random 24 byte string - can use following command to generate a random key : python -c 'import secrets; print(secrets.token_hex())'
    - ways to declare:
    1. docker build argument `docker build --build-arg SECRET_KEY=xxSUPERSECRETxx https://github.com/RT-Tap/booksyCORSproxy -t booksyCORSproxy`
    2. environment variable  - docker-compose, sysem wide, etc.

- BOOKSYAPI_BUSREF: (default:None-Needs to be set) The 6 digit ID of the business you want reviews for, See "Booksy Business Refrence/ID Number" section below
- BOOKSYAPI_PROXY: (True/False - default: false)  - Will this be behind a reverse proxy?
- SERVER_NAME: (default:None-Needs to be set ) URL endpoint of website you intend to use this on eg. "booksyAPItest.com" - used to set our own CORS policy during production
- TLS: (TRUE/FALSE/mutual-default:false)

    - true = what you think of when you think TLS/HTTPS, will use certificate & key passed in from a rootCA (letsencrypt)
    - mutual = zero confidence system where the server validates the client as well, the only difference here is you need to provide the rootCA cert
    - in addition you will need to provide
        - TLS_CERT: (default: docker secret named site.crt) location of signed certificate
        - TLS_KEY: (default: docker secret named site.key) location of private key
        ROOTCA_CERT: (default: docker secret named root.crt) only required for mTLS, location of the root CA certificate

### development / optional
- ROOT_PATH: (optional-default:boorev_api) - Unless you are integrating with another flask app you dont need to worry about this
- FLASK_DEBUG: (optional-True/False default:true) - If you are in development True, production False - IMPORTANT! Used to set our own CORS policy
- booksyAPI_DEBUGSERVER: (optional-Flask/gunicorn default: development=Flask production=gunicorn)
- DEBUG_EXAMPLEREVIEWS: (optional-True/Flase default:false) - when set to true will ONLY retrieve local example reviews (located in sample/samplereviews.txt ) usefull if you plan on working in a live environment constantly reloading/refreshing and therefore repeatedly requesting the same data from booksy but don't want to hit their request limits/raise suspicion
- FLASK_APP: (optional- default: booksyAPI) - will most likely never change, you may break package if changed, used to let know server what application to run
- SERVERCONFIG_BINDADDR: (optional-default:0.0.0.0) - what interface/address to bind to - local only: 127.0.0.1 , all interfaces: 0.0.0.0
- SERVERCONFIG_PORT: (optional-default:5000) - what port to work on
- SERVERCONFIG_WORKERS: (optional- default:20) - amount of worker threads
- SERVERCONFIG_ACCESSLOG: (not fully implemented) (optional - default: stdout) - access log location- will log to stdout but can set to file or syslog ref: https://docs.gunicorn.org/en/20.1.0/settings.html#syslog
- any additional command line argument settings gunicorn takes (https://docs.gunicorn.org/en/20.1.0/settings.html) can simple be appended to the environment variable `GUNICORN_CMD_ARGS`

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
        gunicorn booksyCORSproxy:app 
        ```
- ## Wheel package
    1. set mandatory env vars 
    1. create wheel package
        ```
        cd booksyAPI
        python -m build
        ```
    3. install wheel package
        ```
        pip install dist/booksyCORSproxy-1.1-py3-none-any.whl
        ```
    3. Start Server
        ```
        gunicorn booksyCORSproxy:app
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
