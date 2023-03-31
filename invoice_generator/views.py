import csv
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
import pandas as pd
from django.http import HttpResponse
from .models import Ride
from pathlib import Path
import os
from django.conf import settings
import random
import time
from django.utils.html import escape

csv_file_path = os.path.join(settings.BASE_DIR, "rides.csv")

def home(request):
    
    return render(request, 'home.html')


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

    # delete empty rows
    for row in data:
        if len(row) == 0:
            data.remove(row)
            


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


def log_ride(request):
    if request.method == 'POST':
        id5 = random_id5()
        day = request.POST['day']
        date = request.POST['date']
        time = request.POST['time']
        customer = request.POST['customer']
        contact_number = request.POST['contact_number']
        pick_up_address = request.POST['pick_up_address']
        drop_off_address = request.POST['drop_off_address']
        driver_name = request.POST['driver_name']
        driver_badge = request.POST['driver_badge']
        vehicle_reg = request.POST['vehicle_reg']
        license_vehicle = request.POST['license_vehicle']
        fare = request.POST['fare']
        payment_type = request.POST['payment_type']
        date_booked = request.POST['date_booked']
        time_booked = request.POST['time_booked']
        status = request.POST['status']
        job_source = request.POST['job_source']
        '''
        ride = Ride(
            day=day,
            date=date,
            time=time,
            customer=customer,
            contact_number=contact_number,
            pick_up_address=pick_up_address,
            drop_off_address=drop_off_address,
            driver_name=driver_name,
            driver_badge=driver_badge,
            vehicle_reg=vehicle_reg,
            license_vehicle=license_vehicle,
            fare=fare,
            payment_type=payment_type,
            #date_booked=date_booked,
            time_booked=time_booked,
            status=status,
            job_source=job_source
        )
        ride.save()
'''
        # Write to CSV file
        with open(csv_file_path, mode='a') as file:
            writer = csv.writer(file)
            writer.writerow([id5, day, date, time, customer, contact_number, pick_up_address,
                             drop_off_address, driver_name, driver_badge, vehicle_reg,
                             license_vehicle, fare, payment_type, date_booked, time_booked,
                             status, job_source])

        HttpResponse('Ride logged successfully.')
        return render(request, 'log_ride.html')
    else:
        return render(request, 'log_ride.html')

def view_bookings(request):
    with open(csv_file_path) as csv_file:
        csv_data = csv.reader(csv_file.read().splitlines())
        #csv_data = csv.reader(csv_file)

    data = []
    for row in csv_data:
        # do something with the data in each row
        data.append(row)
    
    # delete empty rows
    for row in data:
        if len(row) == 0:
            data.remove(row)

    # Get the filter criteria from the request parameters
    date_from = request.GET.get('date_from')
    job_source = request.GET.get('job_source')

     # Filter the data based on the filter criteria
    if date_from:
        data = [row for row in data if row[2] >= date_from]

    
    if job_source:
        filtered_data = []
        filtered_data.append(data[0])
        for row in data:
            if (str(row[17]).lower()).strip() == (str(job_source).lower()).strip():
                filtered_data.append(row)

        data = filtered_data

    context = {'data': data}
    if request.method == 'POST':
        print("Invoice data before processing: ", data)
        final_invoice_data = process_data(data)
        print("processed invoice data: ", final_invoice_data)
        
        # Pass CSV data to template
        context = {'data': final_invoice_data, 'to' : request.POST['to'], 'date' : request.POST['invoice_date']}
        return render(request, 'invoice.html', context)

    return render(request, 'view_bookings.html', context)
    
def delete_row(request, id):
    # get the path to the CSV file
    
    # read the CSV file into a list of dictionaries
    with open(csv_file_path, 'r') as f:
        csv_data = csv.reader(f.read().splitlines())
        data = [row for row in csv_data]
    
    # delete empty rows
    for row in data:
        if len(row) == 0:
            data.remove(row)

    # remove the row with the given id from the list
    if str(id).strip() != "data_id".strip():
        data = [row for row in data if row[0] != str(id)]
    
    # write the updated data back to the CSV file
    with open(csv_file_path, 'w', newline='') as f:
        #writer = csv.DictWriter(f, fieldnames=fieldnames)
        #writer.writeheader()
        writer = csv.writer(f)
        writer.writerows(data)
    
    return HttpResponseRedirect(reverse('view_bookings'))

def random_id5():
    id5 = ""
    random.seed(time.time())
    for i in range(5):
        random_int = random.randint(1,9)
        id5 = id5 + str(random_int)
    return id5

def edit_row(request, id):
    
    # read the CSV file into a list 
    with open(csv_file_path, 'r') as f:
        csv_data = csv.reader(f.read().splitlines())
        data = [row for row in csv_data]
    
    # delete empty rows
    for row in data:
        if len(row) == 0:
            data.remove(row)
 
    # find the data row that needs to be edited using the row id
    if str(id).strip() != "data_id".strip():
        row_to_be_edited = []
        for row in data:
            if row[0] == str(id):
                row_to_be_edited = row
                break
    
    form_info_keys = ["day", "date", "time", "customer", "contact_number", "pick_up_address", "drop_off_address", "driver_name", "driver_badge", "vehicle_reg", "license_vehicle", "fare", "payment_type", "date_booked", "time_booked", "status", "job_source"]
    form_info_values = row_to_be_edited[1:]

    form_info_values_escaped = []
    for value in form_info_values:
        if isinstance(value, str):
            form_info_values_escaped.append(escape(value))
        else:
            form_info_values_escaped.append(value)
            
    autofill_values = dict(zip(form_info_keys, form_info_values_escaped))
    
    if request.method == "POST":
            
        id5 = str(id)+ "e"
        day = request.POST['day']
        date = request.POST['date']
        time = request.POST['time']
        customer = request.POST['customer']
        contact_number = request.POST['contact_number']
        pick_up_address = request.POST['pick_up_address']
        drop_off_address = request.POST['drop_off_address']
        driver_name = request.POST['driver_name']
        driver_badge = request.POST['driver_badge']
        vehicle_reg = request.POST['vehicle_reg']
        license_vehicle = request.POST['license_vehicle']
        fare = request.POST['fare']
        payment_type = request.POST['payment_type']
        date_booked = request.POST['date_booked']
        time_booked = request.POST['time_booked']
        status = request.POST['status']
        job_source = request.POST['job_source']

        edited_row = [id5, day, date, time, customer, contact_number, pick_up_address,
                             drop_off_address, driver_name, driver_badge, vehicle_reg,
                             license_vehicle, fare, payment_type, date_booked, time_booked,
                             status, job_source]

        # replace old row with new edited row
        filtered_data = []
        for row in data:
            if row[0] != str(id):
                filtered_data.append(row)
            if row[0] == str(id):
                filtered_data.append(edited_row)
        data = filtered_data 

        with open(csv_file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(data)

        return HttpResponseRedirect(reverse('view_bookings'))
        

    
    return render(request, 'edit.html', {"autofill_values": autofill_values})