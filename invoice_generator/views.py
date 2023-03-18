import csv
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

def upload_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request,'File is not CSV type')
            return HttpResponseRedirect(reverse('upload_csv'))
        
        # Parse CSV file
        data = []
        csv_data = csv.reader(csv_file.read().decode('utf-8').splitlines())
        for row in csv_data:
            data.append(row)

        # Pass CSV data to template
        context = {'data': data}
        return render(request, 'table.html', context)

    return render(request, 'upload_csv.html')


