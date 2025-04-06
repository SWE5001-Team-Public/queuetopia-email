import json


def lambda_handler(event, context):
    for record in event['Records']:
        message_body = record['body']
        print(f"Received message: {message_body}")

        # Example: parse JSON from message body (if needed)
        try:
            data = json.loads(message_body)
            # Process data here
            print(f"Parsed data: {data}")
        except json.JSONDecodeError:
            print("Invalid JSON format in message")

    return {
        'statusCode': 200,
        'body': json.dumps('Processed SQS messages')
    }
