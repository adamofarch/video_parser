from django.shortcuts import render, redirect
from django.conf import settings
import boto3
from boto3.dynamodb.conditions import Attr
from .forms import Vid_Form, search_query_form
from .tasks import process_vid, save_vid, translate_subs
from myapp.utils import search_in_subtitles
import os
import re
import yt_dlp
from django.conf import settings

def index(request):
    form = Vid_Form()
    search_form = search_query_form(request.GET)

    if 'vid_url' in request.POST:
        vid_url = request.POST.get('vid_url')
        youtube_regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        if re.match(youtube_regex, vid_url):
            vid_name = vid_url.split('=')[-1] + '.mp4'

            ydl_opts = {
                'format': 'best',  # Download the best quality available
                'outtmpl': os.path.join(os.path.join(settings.BASE_DIR, "Temp/"), '%(title)s.%(ext)s'),
            } 

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                vid_name = ydl.extract_info(vid_url, download=False)['title'] + '.mp4'
                vid_path = os.path.join(os.path.join(settings.BASE_DIR, 'Temp/'), vid_name)
                ydl.download([f"{vid_url}"])
                request.session['video_name'] = vid_name
                process_vid.delay(vid_path)
                return redirect('success')


    if 'vid_file' in request.FILES:
        form = Vid_Form(request.POST, request.FILES)
        if form.is_valid():
            vid_file = form.cleaned_data['vid_file']
            vid_lang = form.cleaned_data['sub_language']
            vid_url = form.cleaned_data['vid_url']
            os.makedirs(os.path.join(settings.BASE_DIR, 'Temp/'), exist_ok=True)
            vid_serialized_data = vid_file.read()
            vid_name = vid_file.name
            vid_path = os.path.join(os.path.join(settings.BASE_DIR, 'Temp/'), vid_name)
            # Saving the video file locally for ccextractor binary to be executed
            if not os.path.exists(vid_path):
                with open(vid_path, 'wb+') as data:
                    for chunk in vid_file.chunks():
                        data.write(chunk)
                    data.close()
                request.session['video_name'] = vid_name
                # processing the video asynchronously to reduce the HTTP Request Time
                save_vid.delay(vid_name, vid_serialized_data)
                process_vid.delay(vid_path)
                translate_subs.delay(vid_lang, vid_path[:-4] + '.srt')
                return redirect('success')

    elif 'search_query' in request.GET:
        if search_form.is_valid():
            query = search_form.cleaned_data['search_query']
            vid_name = request.session.get('video_name')
            # dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
            # table = dynamodb.Table(vid_name[:-4])
            # response = table.scan(
            #     FilterExpression=Attr('Subs').contains(query.capitalize())
            # )
            
            search_result = search_in_subtitles(query, vid_name[:-4])
            
            return render(request, 'search.html', {'search_form': search_form, 'search_result': search_result})

    context = {'form': form, 'search_form': search_form, 'video_name': request.session.get('video_name')}
    return render(request, 'index.html', context)

def success(request):
    search_form = search_query_form()
    return render(request, 'success.html', {'search_form': search_form})


