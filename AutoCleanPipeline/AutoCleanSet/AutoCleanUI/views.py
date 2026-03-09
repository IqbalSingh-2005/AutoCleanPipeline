from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import UploadedFile
import pandas as pd
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR))

from main import AutoCleanPipeline


def index(request):
    """Display dashboard with latest uploaded file data"""
    latest_file = UploadedFile.objects.first()

    if not latest_file:
        return render(request, 'base.html', {
            'latest_file': None,
            'raw_data': None,
            'summary': None,
            'cleaned_data': None,
        })

    pipeline = AutoCleanPipeline()

    try:
        raw_data = pipeline.load_data(latest_file.file.path)
        summary = pipeline.get_summary()
        cleaned_data = pipeline.clean_all(outlier_column="salary")

        context = {
            'latest_file': latest_file,
            'raw_data': raw_data.to_dict('records')[:10],
            'summary': summary,
            'cleaned_data': cleaned_data.to_dict('records')[:10],
        }

        return render(request, 'base.html', context)

    except Exception as e:
        return render(request, 'base.html', {
            'latest_file': latest_file,
            'error': str(e),
        })


def upload_file(request):
    """Handle file upload"""
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        UploadedFile.objects.create(
            file=uploaded_file,
            filename=uploaded_file.name,
            file_size=uploaded_file.size,
        )
        return redirect('index')

    return redirect('index')


def get_raw_data(request, file_id):
    """Get raw data for a specific file"""
    try:
        file_obj = UploadedFile.objects.get(id=file_id)
        pipeline = AutoCleanPipeline()
        raw_data = pipeline.load_data(file_obj.file.path)

        return JsonResponse({
            'success': True,
            'data': raw_data.to_dict('records'),
            'columns': raw_data.columns.tolist(),
            'shape': raw_data.shape
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def get_summary(request, file_id):
    """Get summary statistics for a specific file"""
    try:
        file_obj = UploadedFile.objects.get(id=file_id)
        pipeline = AutoCleanPipeline()
        pipeline.load_data(file_obj.file.path)
        summary = pipeline.get_summary()

        return JsonResponse({
            'success': True,
            'summary': summary
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def get_cleaned_data(request, file_id):
    """Get cleaned data for a specific file"""
    try:
        file_obj = UploadedFile.objects.get(id=file_id)
        pipeline = AutoCleanPipeline()
        pipeline.load_data(file_obj.file.path)
        cleaned_data = pipeline.clean_all(outlier_column="salary")

        return JsonResponse({
            'success': True,
            'data': cleaned_data.to_dict('records'),
            'columns': cleaned_data.columns.tolist(),
            'shape': cleaned_data.shape
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
