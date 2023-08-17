import os
import logging
import csv
import datetime
import requests
from flask import Flask, render_template
from urllib.parse import urlparse, urlunparse 
from fxdexWallet import WalletConnection

app = Flask(__name__)

PROJECTS = []  # Store project data

PROJECTSAPI=[] 

STATUSWALLET=[]

def check_authenticated_url(url, api_key):
    headers = {
        'x-api-key': api_key
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return True, response.json(), response.status_code
        else:
            return False, response.json(), response.status_code
    except requests.RequestException:
        return False, {'message': 'Fail'}, None

def check_url_status():
    for project in PROJECTS:
        url = project['url']
        try:
            response = requests.head(url)
            project['status'] = response.status_code
            project['status_message'] = 'success'
        except requests.RequestException:
            project['status'] = 'Error'
            project['status_message'] = 'Fail'
        project['last_checked'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

@app.route('/')
def index():
    # Clear the existing data before reading and updating from the CSV file
    PROJECTS.clear()

    # Read data from CSV and update last checked time in memory
    with open('data.csv', 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            project = {
                'project_name': row['Project Name'],
                'url': row['URL'],
                'status': row['Status'],
                'last_checked': row['Last Checked'],
                'status_message': 'No status message'  # Default value
            }
            PROJECTS.append(project)

    check_url_status()

    # Iterate through each row in the API CSV and check the authenticated API
    PROJECTSAPI.clear()
    with open('expandapi.csv', 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            url = row['URL']
            api_key = row['api_key']
            is_successful, response_data, status_code = check_authenticated_url(url, api_key)
            if is_successful:
                status = status_code
            else:
                status = status_code if status_code is not None else 'Failed'

            api_result = {
                'project_name': 'Expand Network',
                'url': url,
                'status': status,
                'last_checked': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'status_message': response_data.get('message', 'success'),
                'apikey': api_key,
            }
            PROJECTSAPI.append(api_result)

    return render_template('index.html', projects=PROJECTS, projectApi=PROJECTSAPI, StatusWallets=STATUSWALLET)

@app.template_filter('url_without_query')
def url_without_query(url):
    parsed_url = urlparse(url)
    clean_url = urlunparse(parsed_url._replace(query=''))
    return clean_url

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
