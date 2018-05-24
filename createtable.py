from __future__ import print_function
import boto3

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

table_exists = False
#IF table exists, then reset the entries
for table in dynamodb.tables.all():
    if table.name == "md5counter":
        table_exists = True
        print("Table already exists, resetting the counters.")
        table.delete_item(Key={ "status": "success"})
        table.delete_item(Key={ "status": "error"})
        table.put_item(Item={ "status": "success","n": 0})
        table.put_item(Item={ "status": "error","n": 0})
        print("Counters reset.")
        break
# IF the table does not exist, then create and populate
if not table_exists:
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
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    # Wait until the table exists.
    table.meta.client.get_waiter('table_exists').wait(TableName='md5counter')

    # Print out some data about the table.
    print("Table 'md5counter' created.")

    # populate the table with our counters.
    table.put_item(Item={ "status": "success","n":0})
    table.put_item(Item={ "status": "error","n": 0})

    print("Table items populated")
