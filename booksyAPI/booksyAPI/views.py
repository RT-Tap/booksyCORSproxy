from asyncio.log import logger
import requests
from flask import request
from flask_api import status
from werkzeug.middleware.proxy_fix import ProxyFix
from booksyAPI import app, logger
import os
import json

@app.route('/')
def index():
    logger.info(f'{request.remote_addr} tried accessing root of API')
    return "Sorry nothing here."

@app.route('/booksyreviews', methods=["GET"])
async def booksyreviews():
    # production:
    json_data =  await get_reviews() if os.getenv("DEBUG_LOCALONLY", "False") == "False" else await get_reviews_development()
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

async def get_reviews():
    try:
        requestURL = 'https://us.booksy.com/api/us/2/customer_api/businesses/' + os.getenv('BOOKSYAPI_BUSREF') + '/reviews/?reviews_page=1&reviews_per_page=20'
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
        logger.warning('Error retreiving reviews from Booksy')
        return False, f"Error retreiving reviews- Remote status code:{r.status_code}"

async def get_reviews_development():
    f = open("./sample/samplereviews.txt", 'r')  # regex find [^\x00-\x7F]+ to remove unicode
    contents = json.loads(json.dumps(f.read()))
    return True, contents

if __name__ == '__main__':
    if os.getenv("booksyAPI_DEBUGSERVER", "Flask") == "Waitress":
        from waitress import serve
        serve(app, host="0.0.0.0", port=5000)
    else:
        import asyncio
        asyncio.run(app.run(debug=True))
