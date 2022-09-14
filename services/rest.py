import logging
import requests
import json
import logging

base_url = "http://drex-env.eba-jkxuyqbq.us-east-1.elasticbeanstalk.com/grid"
record_url = base_url + "/record"


def record_log(body_request):
    _headers = {'Content-Type': 'application/json'}
    try:
        r = requests.post(record_url, data=json.dumps(body_request), headers=_headers)
        #logging.info(f"Operation Successful. status code: {}")
    except requests.exceptions.RequestException as err:
        print('Bad Status Code', r.status_code)
        logging.warning(err)






