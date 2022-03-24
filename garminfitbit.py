#!/usr/bin/env python

import os
import logging
import datetime
import requests
from secret import get_secret

from garminconnect import (
    Garmin,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
    GarminConnectAuthenticationError,
)

class Fitbit:
    def __init__(self, access_token):
        self.access_token = access_token
        self.header = {'Authorization': 'Bearer {}'.format(self.access_token)}
        self.url = 'https://api.fitbit.com/1/user/-/'
    
    def _post(self, api, params):
        return requests.post(self.url + api, params=params, headers=self.header).json()
    
    def _get(self, api, params):
        return requests.post(self.url + api, params=params, headers=self.header).json()

    def post_weight(self, weight, date, time):
        params = {
            'weight': str(weight),
            'date': date,
            'time': time
        }
        response = self._post('body/log/weight.json', params)
        print('Response from fitbit: ', response)
    
    def post_bodyfat(self, fat, date, time):
        params = {
            'fat': str(fat),
            'date': date,
            'time': time
        }
        response = self._post('body/log/fat.json', params)
        print('Response from fitbit: ', response)

# Configure debug logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Fetch credentials
print('Fetching credentials...')

project_id = os.getenv('PROJECT_ID')
FITBIT_ACCESS_TOKEN = get_secret(project_id, 'fitbit_access_token', 1)
GARMIN_CREDENTIALS = str(get_secret(project_id, 'garmin_credentials', 1))
GARMIN_USER, GARMIN_PASS = GARMIN_CREDENTIALS.splitlines()

try:
    # Login to garmin
    print('garmin: logging in');
    garmin = Garmin(GARMIN_USER, GARMIN_PASS)
    garmin.login()
    
    # Download data from garmin for today
    print('garmin: fetching data');
    today = datetime.date.today()
    data = garmin.get_body_composition(today.isoformat())
    garmin.logout()
    
    # Upload data to fitbit
    print('fitbit: uploading');
    fitbit = Fitbit(FITBIT_ACCESS_TOKEN)
    
    for sample in data['dateWeightList']:
        timestamp = int(sample['samplePk']) / 1000
        date_time = datetime.datetime.fromtimestamp(timestamp)    
        time = date_time.strftime("%H:%M:%S")
        date = date_time.strftime("%Y-%m-%d");
        
        try:
            weight = float(sample['weight']) / 1000.0
            fitbit.post_weight(weight, date, time)
        except:
            print("weight is not a number");

        try:
            bodyfat = float(sample['bodyFat'])
            fitbit.post_bodyfat(bodyfat, date, time)
        except:
            print("bodyfat is not a number");
    
except (
        GarminConnectConnectionError,
        GarminConnectAuthenticationError,
        GarminConnectTooManyRequestsError,
    ) as err:
    logger.error("Error occurred during Garmin Connect communication: %s", err)

