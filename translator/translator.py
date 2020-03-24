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


def split(text):
    s = []
    if len(text) > 2500:
        pos = 0
        for i in text:
            if i == "\n":
                break
            pos += 1
        s.append(text[:pos])
        
        if(text[pos + 1:]!=''):
            s+= split(text[pos + 1:])
    else:
        s.append(text)
    return s

w = open("out.txt", "w")
def translate(r):
    texts = split(r)
    first = True
    for text in texts:
        path = '/translate?api-version=3.0'
        params = '&to=de'
        constructed_url = endpoint + path + params

        headers = {
            'Ocp-Apim-Subscription-Key': subscription_key,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }

        body = [
            {"text": text} #2500 max size
        ]

        request = requests.post(constructed_url, headers=headers, json=body)
        response = request.json()

        if first:
            acc_resp = response
            first = False
        else:
            acc_resp[0]['translations'][0]['text']+="\n"+response[0]['translations'][0]['text']

    out = json.dumps(acc_resp, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))
    w.write(out)
    w.close()

#Example
f = open("text.txt", "r")
r = f.read()
f.close()
translate(r)
#output: out.txt