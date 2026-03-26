import argparse
import glob
import logging
import os

import boto3

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def parse_args():
    """ Parse command line args and return the input folder and destination. """
    parser = argparse.ArgumentParser(
        description="Upload results-*.csv files to an S3 bucket prefix."
    )
    parser.add_argument(
        "input_folder",
        help="Folder containing results-*.csv files"
    )
    parser.add_argument(
        "destination",
        help="Destination in the form bucket/prefix/"
    )
    args = parser.parse_args()
    return args.input_folder, args.destination


def upload(input_folder, destination):
    """ Upload all results files from input_folder to the specified destination. """
    try:
        s3 = boto3.client("s3", region_name="us-east-1")

        if "/" in destination:
            bucket, prefix = destination.split("/", 1)
        else:
            bucket = destination
            prefix = ""

        files = glob.glob(os.path.join(input_folder, "results-*.csv"))

        if not files:
            logger.error("No results-*.csv files found in %s", input_folder)
            return False

        for file_path in files:
            filename = os.path.basename(file_path)
            if prefix:
                key = f"{prefix.rstrip('/')}/{filename}"
            else:
                key = filename

            with open(file_path, "rb") as f:
                s3.put_object(
                    Body=f,
                    Bucket=bucket,
                    Key=key
                )

            logger.info("Uploaded %s to s3://%s/%s", filename, bucket, key)

        return True

    except Exception as e:
        logger.error("Upload failed: %s", e)
        return False


def main():
    """ Parse arguments, upload files, and log final. """
    input_folder, destination = parse_args()
    success = upload(input_folder, destination)

    if success:
        logger.info("Upload process completed successfully.")
    else:
        logger.error("Upload process did not complete successfully.")


if __name__ == "__main__":
    main()