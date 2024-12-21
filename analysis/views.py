# analysis/views.py
from django.shortcuts import render
from .forms import UploadFileForm
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import io


def handle_uploaded_file(f):
    # Save the uploaded file to disk temporarily
    with open('temp.csv', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def data_analysis_view(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Read the uploaded CSV file
            uploaded_file = request.FILES['file']
            df = pd.read_csv(uploaded_file)

            # Perform data analysis
            df_head = df.head()  # First few rows
            summary = df.describe()  # Summary statistics
            missing_values = df.isnull().sum()  # Missing values count

            # Convert missing values to a DataFrame for rendering
            missing_values_df = missing_values.reset_index()
            missing_values_df.columns = ['Column', 'Missing Values']

            # Generate a histogram plot
            fig, ax = plt.subplots(figsize=(10, 6))
            df.hist(ax=ax)
            plt.tight_layout()

            # Save the plot to a string buffer
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
            buf.close()

            # Render the results in the template
            context = {
                'form': form,
                'df_head': df_head.to_html(),
                'descriptive_stats': summary.to_html(),
                'missing_values': missing_values_df.to_html(index=False),
                'plot': image_base64,
            }
            return render(request, 'analysis/results.html', context)
    else:
        form = UploadFileForm()

    return render(request, 'analysis/upload.html', {'form': form})
 

