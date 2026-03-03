#!/usr/bin/env python3

import os
import json
import sys
import pandas as pd
import logging
import requests
import mysql.connector
from datetime import datetime

URL = "http://api.open-notify.org/iss-now.json"

# Put your info here
REPORTER_ID = "bvc5vq"
REPORTER_NAME = "Annie Nguyen"

formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logging.basicConfig(level=logging.INFO, handlers=[console_handler])


def get_db():
    host = os.getenv("DBHOST")
    user = os.getenv("DBUSER")
    pwd = os.getenv("DBPASS")

    if not host or not user or not pwd:
        raise RuntimeError("Missing DBHOST/DBUSER/DBPASS environment variables")

    db = mysql.connector.connect(
        host=host,
        user=user,
        password=pwd,
        database="iss",
    )
    cursor = db.cursor()
    return db, cursor


def register_reporter(table, reporter_id, reporter_name):
    """
    Ensure reporter exists in reporters table.
    If reporter_id exists, do nothing (or update name).
    """
    if table != "reporters":
        raise ValueError("register_reporter table must be 'reporters'")

    db = None
    cursor = None
    try:
        db, cursor = get_db()

        # Check existence
        cursor.execute(
            "SELECT reporter_id FROM reporters WHERE reporter_id = %s",
            (reporter_id,),
        )
        row = cursor.fetchone()

        if row is None:
            cursor.execute(
                "INSERT INTO reporters (reporter_id, reporter_name) VALUES (%s, %s)",
                (reporter_id, reporter_name),
            )
            db.commit()
            logging.info(f"Registered reporter: {reporter_id} ({reporter_name})")
        else:
            # Optional: keep name in sync
            cursor.execute(
                "UPDATE reporters SET reporter_name = %s WHERE reporter_id = %s",
                (reporter_name, reporter_id),
            )
            db.commit()
            logging.info(f"Reporter already exists: {reporter_id} (name ensured)")

    except mysql.connector.Error as e:
        logging.error(f"MySQL error in register_reporter: {e}")
        raise
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()


def extract(json_file):
    """
    Request data from ISS API and save raw JSON to a file.
    """
    logging.info(f"Getting data from {URL}")
    data = None

    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
        data = response.json()

        with open(json_file, "w") as f:
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
    Flatten JSON and return a single-row DataFrame.
    """
    logging.info("Cleaning and organizing data...")

    row = {
        "timestamp": raw_data["timestamp"],
        "latitude": raw_data["iss_position"]["latitude"],
        "longitude": raw_data["iss_position"]["longitude"],
        "message": raw_data["message"],
    }

    df = pd.DataFrame([row])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")

    return df


def load(data_rec, reporter_id):
    """
    Insert the latest ISS location record into iss.locations.
    Expects data_rec to be a 1-row DataFrame produced by transform().
    """
    if data_rec is None or data_rec.empty:
        raise ValueError("load() received empty data")

    # Extract values from the dataframe row
    rec = data_rec.iloc[0]

    message = str(rec["message"]) if pd.notna(rec["message"]) else None

    # API gives lat/long as strings; cast to float for DECIMAL(10,4)
    latitude = float(rec["latitude"]) if pd.notna(rec["latitude"]) else None
    longitude = float(rec["longitude"]) if pd.notna(rec["longitude"]) else None

    # Format timestamp as MySQL DATETIME string
    ts = rec["timestamp"]
    if pd.isna(ts):
        timestamp_str = None
    else:
        # ts is a pandas Timestamp
        timestamp_str = ts.strftime("%Y-%m-%d %H:%M:%S")

    db = None
    cursor = None
    try:
        db, cursor = get_db()

        cursor.execute(
            """
            INSERT INTO locations (message, latitude, longitude, timestamp, reporter_id)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (message, latitude, longitude, timestamp_str, reporter_id),
        )
        db.commit()
        logging.info("Inserted a new row into iss.locations")

    except mysql.connector.Error as e:
        logging.error(f"MySQL error in load(): {e}")
        raise
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()


def main():
    """
    Run the ETL pipeline and store results in MySQL.
    Keeps a CLI arg optional; if provided, we use it only for naming the JSON file.
    """
    # Optional arg just to name the json output file
    json_stub = "iss_run"
    if len(sys.argv) > 1:
        # if user passes something like test.csv, we'll create test.json
        json_stub = sys.argv[1].replace(".csv", "").replace(".json", "")

    json_file = f"{json_stub}.json"

    # Ensure reporter exists
    register_reporter("reporters", REPORTER_ID, REPORTER_NAME)

    # ETL
    raw = extract(json_file)
    if raw is None:
        logging.error("Extraction failed. Exiting program.")
        sys.exit(1)

    clean_data = transform(raw)
    load(clean_data, REPORTER_ID)


if __name__ == "__main__":
    main()