import boto3

from app.config.settings import settings

session = boto3.Session(profile_name=str(settings.aws_profile), region_name=str(settings.aws_region))
sqs = session.client("sqs")


def send_message(queue_url: str, message_body: str):
    message = sqs.send_message(QueueUrl=queue_url, MessageBody=message_body)

    return message


def receive_message(queue_url: str):
    response = sqs.receive_message(QueueUrl=queue_url)

    return response

def delete_message(queue_url: str, receipt_handle: str):
    delete = sqs.delete_message(
        QueueUrl=queue_url, 
        ReceiptHandle=receipt_handle
        )
    
    return delete
