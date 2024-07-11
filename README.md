Example engine:

```python
import requests
import zipfile
import os
import csv
import random

# API endpoints
DOWNLOAD_URL = 'http://127.0.0.1:8000/api/download_solutions/'
UPLOAD_URL = 'http://127.0.0.1:8000/api/upload_results/'

# Authentication credentials (replace with actual credentials)
USERNAME = 'your_admin_username'
PASSWORD = 'your_admin_password'

# Function to run the solution (replace with actual logic)
def run_solution(file_path):
    # Example logic to run the solution and return a random score
    return random.randint(1, 100)

# Download solutions
response = requests.get(DOWNLOAD_URL, auth=(USERNAME, PASSWORD))

if response.status_code == 200:
    # Save the downloaded zip file
    with open('solutions.zip', 'wb') as f:
        f.write(response.content)

    # Extract the solutions and metadata
    with zipfile.ZipFile('solutions.zip', 'r') as zip_ref:
        zip_ref.extractall('solutions')

    # Read metadata from metadata.csv
    metadata_path = os.path.join('solutions', 'metadata.csv')
    results = []
    with open(metadata_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            username = row['Username']
            filename = row['Filename']
            file_path = os.path.join('solutions', filename)
            # Load and run the solution (implement your logic here)
            score = run_solution(file_path)  # Replace with your actual scoring function
            results.append({'Username': username, 'Score': score})

    # Upload results
    results_file = 'results.csv'
    with open(results_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['Username', 'Score'])
        writer.writeheader()
        writer.writerows(results)

    with open(results_file, 'rb') as f:
        response = requests.post(UPLOAD_URL, files={'file': f}, auth=(USERNAME, PASSWORD))

    if response.status_code == 200:
        print('Results uploaded successfully.')
    else:
        print('Failed to upload results:', response.content)
else:
    print('Failed to download solutions:', response.content)
```