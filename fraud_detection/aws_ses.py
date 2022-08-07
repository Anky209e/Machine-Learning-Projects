import boto3
from botocore.exceptions import ClientError
import os

print("Loading Credentials...")
# aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
# aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
# if aws_secret_access_key is None or aws_access_key_id is None:
#     print("Credentials not found! You can't sent mails")
# else:
#     print("Credentials Loaded!")

def send_mail(sender,reciever,subject,content_text,content_html):
    SENDER = sender
    RECIPIENT = reciever

    # region
    AWS_REGION = "ap-south-1"
    SUBJECT = subject
    BODY_TEXT = content_text
    BODY_HTML = content_html
    CHARSET = "UTF-8"
    print("Loading Client....")
    client = boto3.client('ses',region_name=AWS_REGION)
    try:
    #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,)
    
# Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
