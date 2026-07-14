import os
import boto3
from fastapi import FastAPI, UploadFile
from prometheus_client import make_asgi_app, Counter

app = FastAPI()

app.mount("/metrics", make_asgi_app())
UPLOAD_COUNTER = Counter('images_uploaded_total', 'Total images uploaded')

s3 = boto3.client('s3', endpoint_url="http://localstack:4566")

@app.on_event("startup")
def setup():
    try:
        s3.create_bucket(Bucket=os.getenv('S3_BUCKET_NAME'))
    except:
        pass

@app.post("/upload")
def upload(file: UploadFile):
    s3.upload_fileobj(file.file, os.getenv('S3_BUCKET_NAME'), file.filename)
    UPLOAD_COUNTER.inc()
    return {"message": "Uploaded successfully", "file": file.filename}