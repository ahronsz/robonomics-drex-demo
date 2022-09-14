import logging
import requests
import json
import logging

base_url = "http://drex-env.eba-jkxuyqbq.us-east-1.elasticbeanstalk.com/grid"
record_url = base_url + "/record"


def record_log(body_request):
    _headers = {'Content-Type': 'application/json'}
    try:
        print("entra a rest")
        print(body_request)
        r = requests.post(record_url, data=json.dumps(body_request), headers=_headers)
        logging.info("Operation Successful. status code: ", r.status_code())
    except requests.exceptions.RequestException as err:
        print('Bad Status Code', r.status_code)
        logging.warning(err)
<





