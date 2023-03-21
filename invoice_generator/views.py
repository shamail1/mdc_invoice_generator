import csv
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
import pandas as pd

def upload_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']

        # Parse CSV file
        data = []
        if csv_file.name.endswith('.csv'):
            csv_data = csv.reader(csv_file.read().decode('utf-8').splitlines())
            for row in csv_data:
                data.append(row)
        elif csv_file.name.endswith('.xlsx'):
            df = (pd.read_excel(csv_file, header=None, dtype=str)).values
            data = df.tolist()
        else:
            #messages.error(request,'File is not CSV or xlsx type')
            return HttpResponseRedirect(reverse('upload_csv'))
            
        print("Invoice data before processing: ", data)
        final_invoice_data = process_data(data)
        print("processed invoice data: ", final_invoice_data)
        
        # Pass CSV data to template
        context = {'data': final_invoice_data, 'to' : request.POST['to'], 'date' : request.POST['invoice_date'] }
        return render(request, 'invoice.html', context)

    return render(request, 'upload_csv.html')

def process_data(data):
    data_required_col = []
    data_col_names = data[0]
    wanted_col_names = ["Date", "Time", "Customer", "Pick up Address", "Drop off Address", "Fare"]

    print("Wanted coloumn names:", wanted_col_names)

    # creating a list of coloumns
    for i in range(len(wanted_col_names)):
        for j in range(len(data_col_names)):
            if str(data[0][j]).replace(" ", "") == str(wanted_col_names[i]).replace(" ", ""):
                c_list = []
                for k in range(len(data)):
                    c_list.append(data[k][j])
                data_required_col.append(c_list)
    
    print("during processing - list of coloumns:", data_required_col)

    # creating a list of rows    
    final_processed_data = []
    for i in range(len(data_required_col[0])):
        c_list = []
        for j in range(len(data_required_col)):
            c_list.append(data_required_col[j][i])
        final_processed_data.append(c_list)
        
    return final_processed_data


