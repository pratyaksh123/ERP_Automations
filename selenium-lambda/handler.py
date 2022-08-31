from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json
import boto3
from datetime import datetime


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
          <p>There is a update regarding your delhivery order:<p>
          <p>{ulify(update)}<p>
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


def main(event, context):
    options = Options()
    options.binary_location = '/opt/headless-chromium'
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--single-process')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome('/opt/chromedriver', chrome_options=options)
    driver.get('https://www.delhivery.com/track/package/2827715726000')
    html = driver.page_source

    soup = BeautifulSoup(html)
    updates = []
    table = soup.find_all('tbody')[1]
    for tag in table:
        if (tag.text != ""):
            updates.append(tag.text)

    driver.close()
    driver.quit()

    bucket = 'order-info-delhivery'
    key = 'data.json'
    s3 = boto3.resource('s3')

    data = lambda_handler(bucket, key, s3)
    list1 = data['delivery_status']
    list2 = updates
    print(list2)
    new_list = []
    for i in list2:
        if i not in list1:
            new_list.append(i)
    if new_list != []:
        # new update detected, send email thorough SES and also update the bucket
        email_handler(new_list)
        s3.Object(bucket, key).put(
            Body=json.dumps({'delivery_status': updates}))

    response = {
        "statusCode": 200,
        "body": updates,
        "differences": new_list
    }

    return response


def lambda_handler(bucket, key, s3):
    obj = s3.Object(bucket, key)
    data = obj.get()['Body'].read().decode('utf-8')
    json_data = json.loads(data)
    return json_data
