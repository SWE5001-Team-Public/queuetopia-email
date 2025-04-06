import json
import os
import resend
from dotenv import load_dotenv

load_dotenv(".env.production")

resend.api_key = os.environ["RESEND_API_KEY"]


def read_email_template():
  with open('email.html', 'r') as file:
    return file.read()


def lambda_handler(event, context):
  for record in event['Records']:
    message_body = record['body']
    print(f"Received message: {message_body}")

    try:
      data = json.loads(message_body)

      # Read email template
      email_template = read_email_template()

      # Replace placeholders with actual data
      personalized_email = (
        email_template
        .replace('{{CompanyName}}', "QueueTopia")
        .replace('{{Name}}', f"{data['first_name']} {data['last_name']}")
        .replace('{{Email}}', data['email'])
        .replace('{{ConfirmationUrl}}', "http://queuetopia-ui.vercel.app/confirm?email=" + data['email'])
      )

      params: resend.Emails.SendParams = {
        "from": "Queuetopia <no-reply@notification.webdevsolutions.io>",
        "to": [data["email"]],
        "subject": "[QueueTopia] You're almost there!",
        "html": personalized_email,
      }

      email = resend.Emails.send(params)
      print(f"Email sent: {email}")
    except json.JSONDecodeError:
      print("Invalid JSON format in message")

  return {
    'statusCode': 200,
    'body': json.dumps('Processed SQS messages')
  }
