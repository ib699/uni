import boto3
from dotenv import load_dotenv
import os


load_dotenv()

LIARA_ENDPOINT = os.getenv("LIARA_ENDPOINT")
LIARA_ACCESS_KEY = os.getenv("LIARA_ACCESS_KEY")
LIARA_SECRET_KEY = os.getenv("LIARA_SECRET_KEY")
LIARA_BUCKET_NAME = os.getenv("LIARA_BUCKET_NAME")

s3 = boto3.client(
        "s3",
        endpoint_url=LIARA_ENDPOINT,
        aws_access_key_id=LIARA_ACCESS_KEY,
        aws_secret_access_key=LIARA_SECRET_KEY,
)


def upload(file):
    s3.upload_fileobj(file, LIARA_BUCKET_NAME, file.filename)


def download(file_name):
    s3.download_file(LIARA_BUCKET_NAME, file_name, file_name)
