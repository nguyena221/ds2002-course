#!/usr/bin/env python3

import os
import json
import sys
import pandas as pd
import logging
import requests

URL = "http://api.open-notify.org/iss-now.json"

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logging.basicConfig(level=logging.INFO, handlers=[console_handler])

def extract(json_file):
    """    
    Data is requested from the ISS API. Handles request errors and returns the parsed JSON data. 
    """
    logging.info(f"Getting data from {URL}")
    data = None
    
    try:
        response = requests.get(URL)
        response.raise_for_status() # raise an exception for HTTP errors
        data = response.json()
        
        with open(json_file, 'w') as f:
            json.dump(data, f, indent=2)
        logging.info(f"Extracted raw data and saved to {json_file}")
    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        logging.error(f"A request error occurred: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

    return data

def transform(raw_data):
    """    
    Accepts raw JSON data from extract(). Flattens the nested structure and selects relevant fields. 
    Timestamp is converted to a readable datetime format. And, returns a single-row pandas DataFrame with the cleaned data.
    """
    logging.info("Cleaning and organizing data...")

    row = {
        "timestamp": raw_data["timestamp"],
        "latitude": raw_data["iss_position"]["latitude"],
        "longitude": raw_data["iss_position"]["longitude"],
        "message": raw_data["message"]
    }

    df = pd.DataFrame([row])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit='s')

    return df

def load(data_rec, output_name):
    """    
    Accepts the cleaned data from transform() and saves it to a CSV file. Checks if the file exists and appends data to file. 
    If file does not exist, creates a new file.
    """
    if (os.path.exists(output_name)):
        data_rec.to_csv(output_name, mode='a', header=False, index=False)
    else: 
        data_rec.to_csv(output_name, index=False)
    
    logging.info(f"Saved cleaned data to {output_name}")

def main():
    """
    Coordinates the ETL workflow by retrieving the output file name from the command line,
    calling the extract, transform, and load functions in sequence, and building the ISS
    location dataset.
    """
    
    try:
        OUTPUT = sys.argv[1] 
    except IndexError:
        logging.error(f"Usage: python {sys.argv[0]} <output_file>")
        sys.exit(1)

    json_file = OUTPUT.replace(".csv", "") + ".json"

    raw = extract(json_file)

    if raw is None:
        logging.error("Extraction failed. Exiting program.")
        sys.exit(1)

    clean_data = transform(raw)
    load(clean_data, OUTPUT)

if __name__ == "__main__":
    main()