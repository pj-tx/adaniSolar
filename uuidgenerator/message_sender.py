import boto3
from botocore.exceptions import ClientError
from rest_framework.response import Response

import os
from dotenv import load_dotenv
load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY_ID = os.getenv('AWS_SECRET_KEY_ID')
AWS_REGION = os.getenv('AWS_REGION')


# Replace sender@example.com with your "From" address.
# This address must be verified with Amazon SES.
def email_ses_sender(recipient, subject, body):
    SENDER = "AGEL Survey <notifications@talocity.in>"

    # Replace recipient@example.com with a "To" address. If your account 
    # is still in the sandbox, this address must be verified.
    RECIPIENT = recipient
    # Specify a configuration set. If you do not want to use a configuration
    # set, comment the following variable, and the 
    # ConfigurationSetName=CONFIGURATION_SET argument below.
    # CONFIGURATION_SET = "ConfigSet"

    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = "us-east-1"

    # The subject line for the email.
    SUBJECT = subject

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = body

    BODY_HTML = f"""<html>
        <head></head>
        <body>
        {body}
        </body>
        </html>
    """     
                
    # The HTML body of the email.          

    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses',aws_access_key_id=AWS_ACCESS_KEY_ID,aws_secret_access_key=AWS_SECRET_KEY_ID,region_name=AWS_REGION)

    # Try to send the email.
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
                    'Html':{
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    }
                    
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
            # If you are not using a configuration set, comment or delete the
            # following line
            # ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        data = e.response['Error']['Message']
        print("Error Ocucred sedning mail")
        print(data)
        return Response(data={"success":False ,"Error":data}, status=400)
    else:
        return {"success":True , "message":response['MessageId']}


