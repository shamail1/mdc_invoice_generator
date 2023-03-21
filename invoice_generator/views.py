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
        
        print("shamail is here ", request.POST['to'])
        # Parse CSV file
        data = []
        csv_data = csv.reader(csv_file.read().decode('utf-8').splitlines())
        print("shamail debug: ",type(csv_data))
        for row in csv_data:
            data.append(row)
        
        final_invoice_data = process_data(data)
        
        # Pass CSV data to template
        context = {'data': final_invoice_data, 'to' : request.POST['to'], 'date' : request.POST['invoice_date'] }
        return render(request, 'invoice.html', context)

    return render(request, 'upload_csv.html')

def process_data(data):
    data_required_col = []
    data_col_names = data[0]
    wanted_col_names = ["Date", "Time", "Customer", "Pick up Address", "Drop off Address", "Fare"]

    for i in range(len(wanted_col_names)):
        for j in range(len(data_col_names)):
            if str(data[0][j]).replace(" ", "") == str(wanted_col_names[i]).replace(" ", ""):
                c_list = []
                for k in range(len(data)):
                    c_list.append(data[k][j])
                data_required_col.append(c_list)

    print("sham is herre",data_required_col)    
    final_processed_data = []
    for i in range(len(data_required_col[0])):
        c_list = []
        for j in range(len(data_required_col)):
            c_list.append(data_required_col[j][i])
        final_processed_data.append(c_list)
        
    return final_processed_data


