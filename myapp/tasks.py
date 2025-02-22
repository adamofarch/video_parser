from celery import shared_task
import subprocess
import os
from django.core.files.base import ContentFile
from .utils import object_exists_in_s3, save_subtitles_to_dynamodb
from .models import Vid

@shared_task
def process_vid(vid_path):
    sub_path =  vid_path[:-4] + '.srt'
    vid_name = os.path.basename(vid_path)[:-4]
    command = ['ccextractor', vid_path, '-o', sub_path]
    response = subprocess.run(command, check=True)
    # os.remove(vid_path)
    return response.stdout
    # Cleaning up the locally stored files 

@shared_task
def save_vid(vid_file_name, serialized_data):
    vid = Vid()
    vid.vid_file.save(vid_file_name, ContentFile(serialized_data))
    vid.save()
