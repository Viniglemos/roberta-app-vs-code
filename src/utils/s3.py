# src/utils/s3.py

import boto3
from botocore.client import Config
from typing import Optional

# 🔴 CHANGE THIS TO YOUR REAL REGION + BUCKET
AWS_REGION = "us-east-1"  # ex: us-east-1, sa-east-1, etc.
S3_BUCKET_NAME = "roberta-app"  # ex: roberta-wedding-photos


def get_s3_client():
    """
    Return an S3 client using the default credentials (env vars, aws configure, etc.).
    """
    if not S3_BUCKET_NAME:
        # This error text is VERY specific; if you still see it, we know this file is being used.
        raise RuntimeError("S3_BUCKET_NAME is EMPTY in src/utils/s3.py")

    # boto3 vai pegar as credenciais de:
    # - AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY (export)
    # - OU ~/.aws/credentials (aws configure)
    session = boto3.session.Session(region_name=AWS_REGION)
    return session.client(
        "s3",
        config=Config(signature_version="s3v4"),
    )


def upload_fileobj_to_s3(fileobj, key: str, content_type: Optional[str] = None):
    """
    Upload a file-like object to S3 at the given key.
    """
    if not S3_BUCKET_NAME:
        raise RuntimeError("S3_BUCKET_NAME is EMPTY in src/utils/s3.py")

    extra_args = {}
    if content_type:
        extra_args["ContentType"] = content_type

    s3 = get_s3_client()
    s3.upload_fileobj(
        Fileobj=fileobj,
        Bucket=S3_BUCKET_NAME,
        Key=key,
        ExtraArgs=extra_args or None,
    )


def generate_presigned_url(key: str, expires_in: int = 3600) -> str:
    """
    Generate a presigned URL to access an S3 object.
    """
    if not S3_BUCKET_NAME:
        raise RuntimeError("S3_BUCKET_NAME is EMPTY in src/utils/s3.py")

    s3 = get_s3_client()
    return s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": S3_BUCKET_NAME, "Key": key},
        ExpiresIn=expires_in,
    )
