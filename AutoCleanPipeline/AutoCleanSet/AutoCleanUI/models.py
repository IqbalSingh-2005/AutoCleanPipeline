from django.db import models
from django.utils import timezone

# Create your models here.

class UploadedFile(models.Model):
    """
    Model to store uploaded data files for cleaning and visualization.

    Fields:
        file: The uploaded file (CSV, Excel, JSON, etc.)
        filename: Original name of the uploaded file
        file_size: Size of the file in bytes
        uploaded_at: Timestamp when file was uploaded
        processed: Whether the file has been processed/analyzed
    """
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')
    filename = models.CharField(max_length=255)
    file_size = models.BigIntegerField(help_text="File size in bytes")
    uploaded_at = models.DateTimeField(default=timezone.now)
    processed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Uploaded File'
        verbose_name_plural = 'Uploaded Files'

    def __str__(self):
        return f"{self.filename} ({self.get_file_size_display()})"

    def get_file_size_display(self):
        """Return human-readable file size."""
        size = self.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.2f}{unit}"
            size /= 1024.0
        return f"{size:.2f}TB"
