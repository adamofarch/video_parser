import boto3
from django.conf import settings

def object_exists_in_s3(vid_file_name):
    s3 = boto3.client('s3')
    response = s3.list_objects(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
    if 'Contents' in response:
        for obj in response['Contents']:
            if obj['Key'] == vid_file_name:
                return True
            else:
                return False
    else:
        return False


def save_subtitles_to_dynamodb(subtitle_path, vid_file_name):
    dynamodb = boto3.client('dynamodb', region_name='ap-south-1')
    response = dynamodb.list_tables()

    if not vid_file_name in response['TableNames']:
        dynamodb.create_table(
            TableName=vid_file_name,
            KeySchema=[
                {
                    'AttributeName': 'TimeStamp',
                    'KeyType': 'HASH'
                }

            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'TimeStamp',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }

        )
        settings.DYNAMODB.Table(vid_file_name).wait_until_exists()
        
    table = settings.DYNAMODB.Table(vid_file_name)
    with open(subtitle_path, 'r') as f:
        data = f.read()

    entries = data.strip().split('\n\n')
    for entry in entries:
        lines = entry.split('\n')
        if len(lines) >= 3:
            timestamp = lines[1]
            sub_text = ''.join(lines[2:]).strip()
            table.put_item(
                Item={
                    'TimeStamp': timestamp,
                    'Subs': sub_text.lower()
                }
            )
    f.close()



