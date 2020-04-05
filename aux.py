# -*- coding: utf-8 -*-

import os, requests, uuid, json, csv

key_var_name = 'TRANSLATOR_TEXT_SUBSCRIPTION_KEY'
if not key_var_name in os.environ:
    raise Exception('Please set/export the environment variable: {}'.format(key_var_name))
subscription_key = os.environ[key_var_name]

endpoint_var_name = 'TRANSLATOR_TEXT_ENDPOINT'
if not endpoint_var_name in os.environ:
    raise Exception('Please set/export the environment variable: {}'.format(endpoint_var_name))
endpoint = os.environ[endpoint_var_name]


# f = open("text.txt", "r")
text = "Alhambra Palace"


path = '/translate?api-version=3.0'
params = '&to=de&to=es'
constructed_url = endpoint + path + params

headers = {
    'Ocp-Apim-Subscription-Key': subscription_key,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}

body = [
    {"text": text[:2500]} #2500 max size
]

request = requests.post(constructed_url, headers=headers, json=body)
response = request.json()

print(json.dumps(response, sort_keys=True, indent=4, separators=(',', ': ')))
# out = json.dumps(response, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))

# f.close()

# w = open("out.txt", "w")
# w.write(out)
# w.close()