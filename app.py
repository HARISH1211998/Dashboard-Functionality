import os
import csv
import datetime
import requests
from flask import Flask, render_template

app = Flask(__name__)

PROJECTS = []  # Store project data


def check_url_status():
    for project in PROJECTS:
        url = project['url']
        try:
            response = requests.head(url)
            project['status'] = response.status_code
        except requests.RequestException:
            project['status'] = 'Error'
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
                'last_checked': row['Last Checked']
            }
            PROJECTS.append(project)

    check_url_status()

    return render_template('index.html', projects=PROJECTS)


if __name__ == '__main__':
    app.run(debug=True)
