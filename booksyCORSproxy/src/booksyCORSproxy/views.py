from asyncio.log import logger
import requests
from flask import request
from flask_api import status
from werkzeug.middleware.proxy_fix import ProxyFix
import os
import json
from booksyCORSproxy import app, logger

@app.route('/')
def index():
    logger.info(f'{request.remote_addr} tried accessing root of API')
    return "Sorry nothing here."

@app.route('/healthcheck', methods=["GET"])
async def dockerhealthcheck():
    logger.debug("Docker healthcheck requested.")
    return "still running smooth", status.HTTP_204_NO_CONTENT

@app.route('/booksyreviews/<businessID>', methods=["GET"])
async def booksyreviews(businessID):
    # production:
    json_data =  await get_reviews(businessID) if os.getenv("DEBUG_USEEXAMPLEREVIEWS", "false").lower() == "false" else await get_reviews_development()
    if json_data[0] is True:
        return json_data[1],  status.HTTP_200_OK
        # -----CORS solution option 2 of 2-----
        # response = json_data[1].text
        # response.headers.add("Access-Control-Allow-Origin", "*")
        # return response, 200
    else:
        if len(json_data) <= 1 :
            return "internal service error",  status.HTTP_500_INTERNAL_SERVER_ERROR 
        else:
            return json_data[1], status.HTTP_503_SERVICE_UNAVAILABLE

async def get_reviews(businessID):
    try:
        requestURL = 'https://us.booksy.com/api/us/2/customer_api/businesses/' + str(businessID) + '/reviews/?reviews_page=1&reviews_per_page=20'
        r = requests.get(requestURL, headers={'Accept':'application/json', 'x-api-key':'web-e3d812bf-d7a2-445d-ab38-55589ae6a121'})
    except requests.exceptions.RequestException as e:
        logger.warning(f'Error retrieving review data from Booksy\nError: {e}')
        return False
    if r.status_code >=200 and r.status_code <= 300:
        data = r.json()
        if "reviews" not in data:
            logger.warning('Unexpected Response from Booksy')
            return False, "Unexpected Response from Booksy"
        else: 
            return True, r.text
    else:
        logger.warning('Error retreiving reviews from Booksy, 6-digit business refrence code may be wrong ')
        return False, f"Error retreiving reviews, 6-digit business refrence code may be wrong - Remote status code:{r.status_code}"

# development/debug endpoint - provide your own reviews so you arent constantly requesting from booksy and either hitting a rate limit or alerting them 
async def get_reviews_development():
    try:
        f = open("./sample/samplereviews.txt", 'r')  
        contents = json.loads(json.dumps(f.read())) # to remove unicode use regex [^\x00-\x7F]+ 
        f.close()
    except:
        contents = "Sory file doesnt exist"
    return True, contents
