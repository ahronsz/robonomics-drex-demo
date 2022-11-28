import requests
import json
import logging

def record_log(body_request):
    base_url = "http://drex-env.eba-jkxuyqbq.us-east-1.elasticbeanstalk.com/grid"
    _url = base_url + "/record"
    try:
        response = requests.post(
            url = _url, 
            data = json.dumps(body_request), 
            headers = {'Content-Type': 'application/json'}
        )
        response.raise_for_status()
        logging.info(f"Data grid sent: {body_request}")
    except requests.exceptions.HTTPError as e:
        logging.error("Api Exception: {}".format(e))
    except requests.exceptions.RequestException as e:
        logging.error("Failed to establish connection to the backend")