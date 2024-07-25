import boto3
import os

sqs_client =boto3.client("sqs", region_name="ap-south-1",
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
                   aws_secret_access_key=os.environ.get('AWS_SECRET_KEY'))
def create_queue(sqs_client):
    
    response = sqs_client.create_queue(
        QueueName="product_transaction",
        Attributes={
            "DelaySeconds": "0",
            "VisibilityTimeout": "60",  # 60 seconds
        }
    )


def sendMessage(sqs_client):
    try:
         queue = sqs_client.get_queue_url(QueueName='product_transaction')
         response = sqs_client.send_message(
             QueueUrl=queue['QueueUrl'],
             DelaySeconds=10,
             MessageAttributes=[
                {
                    'id': 1,
                    'quantity': 1
                },
                {
                    'id': 3,
                    'quantity': 5
                },
                
            ],
            MessageBody=("Order placed")
        )   

    except Exception as e:
        print("Error in sending message \n{}".format(e))
        return None


def getMessage():
    try:
        queue = sqs_client.get_queue_url(QueueName='product_transaction')
        response = sqs_client.receive_message(
            QueueUrl=queue['QueueUrl'],
            AttributeNames=[
                'SentTimestamp'
            ],
            MaxNumberOfMessages=1,
            MessageAttributeNames=[
                'All'
            ],
            VisibilityTimeout=0,
            WaitTimeSeconds=10
        )

        message = response['Messages'][0]
        print(message)
    except Exception as e:
        print("Error in recieving message \n{}".format(e))
        return None




