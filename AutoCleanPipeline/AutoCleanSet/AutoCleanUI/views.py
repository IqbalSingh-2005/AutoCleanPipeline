from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .models import UploadedFile
import pandas as pd
import sys
from pathlib import Path
import io
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR))

from main import AutoCleanPipeline
from src.visualizer import generate_chart, get_all_columns, get_numeric_columns
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')


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
        cleaned_data = pipeline.clean_all(outlier_column=None)

        # Get column information
        all_columns = get_all_columns(cleaned_data)
        numeric_columns = get_numeric_columns(cleaned_data)

        # Generate default chart if we have data
        default_chart = None
        if len(numeric_columns) >= 2:
            try:
                default_chart = generate_chart(
                    cleaned_data, 
                    numeric_columns[0], 
                    numeric_columns[1], 
                    'line'
                )
            except:
                pass

        context = {
            'latest_file': latest_file,
            'raw_data': raw_data.to_dict('records')[:10],
            'summary': summary,
            'cleaned_data': cleaned_data.to_dict('records')[:10],
            'all_columns': all_columns,
            'numeric_columns': numeric_columns,
            'default_chart': default_chart,
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


def generate_chart_ajax(request):
    """Generate chart dynamically via AJAX"""
    if request.method == 'POST':
        try:
            x_col = request.POST.get('x_column')
            y_col = request.POST.get('y_column')
            chart_type = request.POST.get('chart_type', 'line')

            latest_file = UploadedFile.objects.first()
            if not latest_file:
                return JsonResponse({'success': False, 'error': 'No file uploaded'})

            pipeline = AutoCleanPipeline()
            pipeline.load_data(latest_file.file.path)
            cleaned_data = pipeline.clean_all(outlier_column=None)

            chart_image = generate_chart(cleaned_data, x_col, y_col, chart_type)

            return JsonResponse({
                'success': True,
                'chart': chart_image
            })

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})


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
        cleaned_data = pipeline.clean_all(outlier_column=None)

        return JsonResponse({
            'success': True,
            'data': cleaned_data.to_dict('records'),
            'columns': cleaned_data.columns.tolist(),
            'shape': cleaned_data.shape
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def download_cleaned_excel(request):
    """Download cleaned data as Excel file"""
    try:
        latest_file = UploadedFile.objects.first()
        if not latest_file:
            return HttpResponse('No file uploaded', status=404)

        pipeline = AutoCleanPipeline()
        pipeline.load_data(latest_file.file.path)
        cleaned_data = pipeline.clean_all(outlier_column=None)

        buffer = io.BytesIO()
        cleaned_data.to_excel(buffer, index=False, engine='openpyxl')
        buffer.seek(0)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'cleaned_data_{timestamp}.xlsx'

        response = HttpResponse(
            buffer.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

    except Exception as e:
        return HttpResponse(f'Error: {str(e)}', status=500)


def download_chart_pdf(request):
    """Download chart as PDF"""
    if request.method == 'POST':
        try:
            x_col = request.POST.get('x_column')
            y_col = request.POST.get('y_column')
            chart_type = request.POST.get('chart_type', 'line')

            latest_file = UploadedFile.objects.first()
            if not latest_file:
                return HttpResponse('No file uploaded', status=404)

            pipeline = AutoCleanPipeline()
            pipeline.load_data(latest_file.file.path)
            cleaned_data = pipeline.clean_all(outlier_column=None)

            fig, ax = plt.subplots(figsize=(10, 6))

            x = cleaned_data[x_col]
            y = cleaned_data[y_col]

            if chart_type == 'line':
                ax.plot(x, y)
            elif chart_type == 'scatter':
                ax.scatter(x, y)
            elif chart_type == 'bar':
                ax.bar(x, y)
            elif chart_type == 'area':
                ax.fill_between(range(len(x)), y, alpha=0.3)
                ax.plot(range(len(x)), y)
            elif chart_type == 'histogram':
                ax.hist(y, bins=20)
            elif chart_type == 'box':
                ax.boxplot([cleaned_data[x_col], cleaned_data[y_col]])

            ax.set_xlabel(x_col)
            ax.set_ylabel(y_col)
            ax.set_title(f'{chart_type.title()} Chart: {x_col} vs {y_col}')
            plt.tight_layout()

            buffer = io.BytesIO()
            fig.savefig(buffer, format='pdf')
            plt.close(fig)
            buffer.seek(0)

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'chart_{chart_type}_{timestamp}.pdf'

            response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response

        except Exception as e:
            return HttpResponse(f'Error: {str(e)}', status=500)

    return HttpResponse('Invalid request method', status=405)
