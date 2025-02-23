from celery import shared_task
import subprocess
from django.conf import settings
import os
from django.core.files.base import ContentFile
from .utils import object_exists_in_s3, save_subtitles_to_dynamodb
from .models import Vid
from googletrans import Translator
from django.shortcuts import render
import re
import time
from requests.exceptions import RequestException
from deep_translator import GoogleTranslator
import pysrt


@shared_task
def process_vid(vid_path):
    sub_path =  vid_path[:-4] + '.srt'
    vid_name = os.path.basename(vid_path)[:-4]
    command = ['ccextractor', vid_path, '-o', sub_path]
    response = subprocess.run(command, check=True)
    os.remove(vid_path)
    return response.stdout
    # Cleaning up the locally stored files 

@shared_task
def save_vid(vid_file_name, serialized_data):
    vid = Vid()
    vid.vid_file.save(vid_file_name, ContentFile(serialized_data))
    vid.save()

@shared_task
def translate_subs(vid_lang, subtitle_path): 
    input_file = subtitle_path
    output_file = os.path.join(os.path.join(settings.BASE_DIR, 'mediafiles'), subtitle_path[:-4]) + '_translated.srt'
    target_lang = vid_lang
    subs = pysrt.open(input_file)

    translator = GoogleTranslator(source='auto', target=target_lang)

    for sub in subs:
        try:
            sub.text = translator.translate(sub.text)
            print(sub.text)
        except Exception as e:
            print(f"Error translating: {sub.text}")
            continue

    subs.save(output_file, encoding='utf-8')

