import os
import pandas as pd
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from .forms import UploadFileForm

def handle_uploaded_file(f):
    # Save the uploaded file to a directory
    upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, f.name)
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return file_path

def process_excel(file_path):
    df = pd.read_excel(file_path)
    summary = df.groupby(['State', 'DPD']).size().reset_index(name='Count')
    return summary

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file_path = handle_uploaded_file(request.FILES['file'])
            request.session['file_path'] = file_path
            return redirect('summary')
    else:
        form = UploadFileForm()
    return render(request, 'excelapp/upload.html', {'form': form})

def summary(request):
    file_path = request.session.get('file_path')
    if not file_path:
        return redirect('upload_file')
    summary_df = process_excel(file_path)
    summary = summary_df.to_dict(orient='records')
    return render(request, 'excelapp/summary.html', {'summary': summary})
