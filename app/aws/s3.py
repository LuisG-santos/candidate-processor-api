import boto3

from app.config.settings import settings


def generate_upload_url(bucket_name: str, s3_key: str) -> str:
    session = boto3.Session(profile_name=str(settings.aws_profile))
    s3 = session.client('s3')

    url = s3.generate_presigned_url(
        ClientMethod="put_object", 
        Params={'Bucket': bucket_name, 'Key': s3_key},
        ExpiresIn=3600
        )
    
    return url
    





