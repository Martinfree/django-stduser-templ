import os
from django.core.exceptions import ValidationError

def validate_file_size(file, max_file_size):
    filesize = os.stat(str(file)).st_size/(1024*1024)
    if filesize > max_file_size:
        raise ValidationError(f"The maximum file size that can be uploaded is {max_file_size}MB")
    else:
        return file
 
