import pandas as pd
from django.shortcuts import render,redirect
from .models import Author, Book
from .forms import UploadFileForm
import pandas as pd
import io
from io import BytesIO

def handle_uploaded_file(f):
    try:
        df = pd.read_excel(io.BytesIO(f.read()), engine='openpyxl')
        return df, None
    except Exception as e:
        return None, str(e)


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            df, error = handle_uploaded_file(file)
            
            if error:
                return render(request, 'error.html', {
                    'error_message': f"Error reading the file: {error}"
                })

            return render(request, 'preview.html', {'data': df.to_html(index=False)})
    else:
        form = UploadFileForm()

    return render(request, 'upload.html', {'form': form})


def confirm_upload(request):
    if request.method == 'POST':
        file = request.session.get('uploaded_file')  
        if not file:
            return redirect('upload_file')

        df = pd.read_excel(BytesIO(file.read()), engine='openpyxl')

        for _, row in df.iterrows():
            author, created = Author.objects.get_or_create(
                name=row['Author Name'],
                email=row['Author Email'],
                date_of_birth=row['Author Date of Birth']
            )
            Book.objects.create(
                name=row['Book Name'],
                isbn_code=row['ISBN Code'],
                author=author
            )

        return render(request, 'success.html')

    return redirect('upload_file')