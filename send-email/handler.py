import json
import boto3

def ulify(elements):
    string = "<ul>\n"
    string += "\n".join(["<li>" + str(s) + "</li>" for s in elements])
    string += "\n</ul>"
    return string


def email_handler(update):
    from_email = "tyagipratyaksh@gmail.com"
    client = boto3.client('ses')

    body_html = f"""<html>
        <head></head>
        <body>
          <p>This was sent from a Python Lambda using Amazon SES</p>
          <p>{update}<p>
        </body>
        </html>"""

    email_message = {
        'Body': {
            'Html': {
                'Charset': 'utf-8',
                'Data': body_html,
            },
        },
        'Subject': {
            'Charset': 'utf-8',
            'Data': "Hello from AWS SES",
        },
    }

    ses_response = client.send_email(
        Destination={
            'ToAddresses': ['tyagi.6@iitj.ac.in'],
        },
        Message=email_message,
        Source=from_email,
    )

    print(f"ses response id received: {ses_response['MessageId']}.")


def hello(event, context):
    event_body = json.loads(event['body'])
    body = {
        "message": "Go Serverless v3.0! Your function executed successfully!",
        "input": event_body['result'],
    }
    email_handler(f"Updated grade: {event_body['result']}")
    response = {"statusCode": 200, "body": json.dumps(body)}
    return response
