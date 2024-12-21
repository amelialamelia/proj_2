from django.shortcuts import render, redirect
from .forms import DataForm
from .models import year_collection, stations_data
import json

def home(request):
    form = DataForm(request.GET or None)
    
    if form.is_valid():
        date = form.cleaned_data['date']
        data_type = form.cleaned_data['data_type']
        if date and data_type:
            return redirect('data_vis', data_type=data_type, date=date)
    context = {'form': form,
               'station_data': stations_data}
    return render(request, "pag_app/home.html", context)


def data_vis(request, data_type, date):
    initial_data = {'date': date, 'data_type': data_type}
    form = DataForm(initial=initial_data)

    if request.GET:
        form = DataForm(request.GET)
        if form.is_valid():
            date = form.cleaned_data['date']
            data_type = form.cleaned_data['data_type']
            if date and data_type:
                return redirect('data_vis', data_type=data_type, date=date)
    
    if data_type == 'year':
        year = date.split('-')[0]
        susza_data = year_collection.find_one({'year': year})
        susza_data = json.dumps(susza_data, default=str)
    elif data_type == 'month':
        susza_data = 0
        
    context = {
        "form": form,
        "station_data": stations_data,
        "susza_data": susza_data
    }
    return render(request, "pag_app/data_vis.html", context)
