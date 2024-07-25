import boto3

# Create an SNS client
sns_client = boto3.client('sns')
phone_number = '+1234567890'
message = "This is a test message sent from noname using Amazon SNS and python."
# Set the topic ARN that the phone number is subscribed to
topic_arn = 'arn:aws:sns:us-east-1:123456789012:MyTopic'


# Send the SMS message
response = sns.publish(
    PhoneNumber=phone_number,
    Message=message,
    TopicArn=topic_arn
)
