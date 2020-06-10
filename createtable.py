from __future__ import print_function
import boto3

# Get the service resource.
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table("md5counter")
try:
    table.creation_date_time
except:
    print("Table does not exist, creating ...")
    # Create the DynamoDB table.
    table = dynamodb.create_table(
        TableName='md5counter',
        KeySchema=[
            {
                'AttributeName': 'status',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'status',
                'AttributeType': 'S'
            }
        ],
        BillingMode='PAY_PER_REQUEST'
    )

    # Wait until the table exists.
    table.wait_until_exists()

    # Print out some data about the table.
    print("Table 'md5counter' created.")

    # populate the table with our counters.
    table.put_item(Item={ "status": "success","n":0})
    table.put_item(Item={ "status": "error","n": 0})

    print("Table items populated")
