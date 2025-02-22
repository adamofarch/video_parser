from django.shortcuts import render, redirect
from django.conf import settings
import boto3
from boto3.dynamodb.conditions import Attr
from .forms import Vid_Form, search_query_form
from .tasks import process_vid, save_vid_to_s3_bucket
import os

def index(request):
    form = Vid_Form(request.POST, request.FILES)
    search_form = search_query_form(request.GET)
    if request.method == 'POST':
        if form.is_valid():
            vid_file = form.cleaned_data['vid_file']
            vid_name = vid_file.name
            vid_serialized_data = vid_file.read()
            vid_path = os.path.join(os.path.join(settings.BASE_DIR, 'Temp/'), vid_name)
            # Saving the video file locally for ccextractor binary to be executed
            if not os.path.exists(vid_path):
                with open(vid_path, 'wb+') as data:
                    for chunk in vid_file.chunks():
                        data.write(chunk)
                data.close()
            request.session['video_name'] = vid_name
            # processing the video asynchronously to reduce the HTTP Request Time
            save_vid_to_s3_bucket.delay(vid_name, vid_serialized_data)
            process_vid.delay(vid_path)
            return redirect('success')
    
    elif 'search_query' in request.GET:
        if search_form.is_valid():
            query = search_form.cleaned_data['search_query']
            vid_name = request.session.get('video_name')
            dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
            table = dynamodb.Table(vid_name[:-4])
            response = table.scan(
                FilterExpression=Attr('Subs').contains(query.capitalize())
            )
            search_result = []
            items = response.get('Items', [])
            for item in items:
                search_result.append(item['TimeStamp'])
            
            return render(request, 'search.html', {'search_form': search_form, 'result': search_result})

    context = {'form': form, 'search_form': search_form}
    return render(request, 'index.html', context)

def success(request):
    search_form = search_query_form()
    return render(request, 'success.html', {'search_form': search_form})


