import boto3
from django.conf import settings
import os
import re


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

def search_in_subtitles(query, video_name):
    """
    Search for query terms in subtitle file corresponding to video_name
    Returns list of matches with timestamp and context
    """
    search_results = []
    subtitle_path = os.path.join(settings.BASE_DIR, 'Temp/') + f"{video_name}.srt"
    
    if not subtitle_path:
        return []
        
    # Read subtitle file
    with open(subtitle_path, 'r', encoding='utf-8') as f:
        content = f.read().lower()
    
    # Split into subtitle blocks
    subtitle_blocks = content.strip().split('\n\n')
    
    for block in subtitle_blocks:
        lines = block.split('\n')
        if len(lines) < 3:  # Skip malformed blocks
            continue
            
        index = lines[0]
        timestamp = lines[1]
        text = ' '.join(lines[2:])  # Combine all text lines
        
        # Case insensitive search
        if re.search(query, text, re.IGNORECASE):
            # Get context around the match
            match_context = {
                'timestamp': timestamp,
                'text': text,
                'index': index
            }
            search_results.append(match_context)
    
    return search_results

