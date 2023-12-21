import json
import boto3

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    client_id_filter = event["queryStringParameters"].get("client_id") if event.get("queryStringParameters") else None
    order_id_filter = event["queryStringParameters"].get("order_id") if event.get("queryStringParameters") else None
    order_id_filter = set(order_id_filter.split(",")) if order_id_filter else None
    bucket_name = "orderapistackstack-orderbucket8884a1db30d-c9uo6u4kxkh4"
    file_key = "orders_file.json"

    # Retrieve order data from specific file in S3 bucket
    orders = []

    # Read file from S3
    try:
        file_content = s3_client.get_object(Bucket=bucket_name, Key=file_key)['Body'].read().decode('utf-8')
        json_content = json.loads(file_content)

        # Assuming json_content is a list of orders
        for order in json_content:
            if matches_filters(order, client_id_filter, order_id_filter):
                orders.append(order)
    except Exception as e:
        print(f"Error reading file from S3: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error reading data'}),
            'headers': {
                'Content-Type': 'application/json'
            }
        }

    return {
        'statusCode': 200,
        'body': json.dumps(orders),
        'headers': {
            'Content-Type': 'application/json'
        }
    }

def matches_filters(order, client_id, order_id):
    client_match = client_id is None or str(order.get("client_id")) == client_id
    order_id_match = order_id is None or str(order.get("order_id")) in order_id
    return client_match and order_id_match

