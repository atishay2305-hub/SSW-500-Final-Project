import json
import requests
import logging 

logging.basicConfig(filename='api_logs.log', filemode='w', level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
questions = {}

try:
    API_URL="https://opentdb.com/api.php"
    params = {"amount":2,"category": 10}

    logging.info("Calling API")

    #get the response from API
    response = requests.get(API_URL,params=params)

    if response.json().get('response_code') == 0: #IF category or amount value is wrong you get error
        questions = json.loads(response.text) #Convert API response to JSON
        logging.info(questions)

    else:
        logging.error("Invalid params or API URL")

except requests.RequestException as e:
    logging.error(f"Request to API failed: {str(e)}")

except Exception as e:
    logging.error(f"An unexpected error occurred: {str(e)}")