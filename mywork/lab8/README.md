# Lab 8 - S3 Storage

## Task 1
Used AWS CLI to create an S3 bucket, upload files, test private access, generate a presigned URL, and upload a public file.

## Task 2
Used boto3 to upload a private file (confirmed AccessDenied) and a public file (confirmed accessible via URL).

## Task 3
Created a Python script (`upload_results.py`) that accepts an input folder and S3 destination, then uploads all `results-*.csv` files to the specified bucket and prefix. 

The script includes argument parsing, logging, and error handling, and was structured according to the assignment requirements. I tested the script by creating a local folder with mock `results-*.csv` files and confirmed that they were successfully uploaded to the `book-analysis/` prefix in my S3 bucket.

Although the script is fully functional, I was unable to use the original Lab 07 output files because the UVA HPC system was unavailable at the time. However, the script was verified to behave correctly using locally generated test files that follow the expected naming pattern.