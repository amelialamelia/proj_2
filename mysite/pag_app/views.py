from django.shortcuts import render, redirect
from .forms import DataForm
from .models import person_collection, stations
import redis
import json

def home(request):
    form = DataForm(request.GET or None)
    
    if form.is_valid():
        date = form.cleaned_data['date']
        data_type = form.cleaned_data['data_type']
        if date and data_type:
            return redirect('data_vis', data_type=data_type, date=date)
    context = {'form': form,
               'station_data': stations}
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
    
    context = {
        "data_type": data_type,
        "date": date,
        "form": form,
        "station_data": stations
    }
    return render(request, "pag_app/data_vis.html", context)
