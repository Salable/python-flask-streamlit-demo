import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

SALABLE_URL = 'https://api.salable.app/licenses'
SALABLE_API_KEY = os.environ.get("SALABLE_API_KEY", "")
SALABLE_PRODUCT_ID = os.environ.get("SALABLE_PRODUCT_ID", "")
SALABLE_PLAN_ID = os.environ.get("SALABLE_PLAN_ID", "")

def check_grantee_id(grantee_id):
    headers = {
        'x-api-key': SALABLE_API_KEY
    }
    response = requests.get(url=f'{SALABLE_URL}/check?productUuid={SALABLE_PRODUCT_ID}&granteeIds=[{grantee_id}]', headers=headers)
    print(response)
    if response.status_code == 200:
        return({
            'status': response.status_code,
            'data': response.json(),
            'licensed' : True
        })
    else:      
        return {
            'status': response.status_code,
            'data': {},
            'licensed' : False
        }

def create_license(grantee_id, member_id):
    headers = {
        'x-api-key': SALABLE_API_KEY
    }
    payload={
        "planUuid": SALABLE_PLAN_ID,
        "member": member_id,
        "granteeId": grantee_id
    }
    response = requests.post(url=f'{SALABLE_URL}', headers=headers, json=payload)
    print(response)
    if response.status_code == 200:
        return({
            'status': response.status_code,
            'data': response.json(),
            'licensed' : True
        })
    else:      
        return {
            'status': response.status_code,
            'data': {},
            'licensed' : False
        }