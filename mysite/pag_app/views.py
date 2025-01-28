from django.shortcuts import render, redirect
from .forms import DataForm
from .models import stations_data, month_collection
import json

def home(request):
    form = DataForm(request.GET or None)
    
    if form.is_valid():
        date = form.cleaned_data['date']
        if date:
            return redirect('data_vis', date=date)
    context = {'form': form,
               'station_data': stations_data}
    return render(request, "pag_app/home.html", context)


def data_vis(request, date):
    initial_data = {'date': date[:-3]}
    form = DataForm(initial=initial_data)
    print(date)
    if request.GET:
        form = DataForm(request.GET)
        if form.is_valid():
            date = form.cleaned_data['date']
            if date:
                return redirect('data_vis', date=date)

    month_id = date[:-3]
    susza_data = month_collection.find_one({'properties.date': month_id})
    susza_data = json.dumps(susza_data, default=str)

    context = {
        "form": form,
        "station_data": stations_data,
        "susza_data": susza_data
    }
    return render(request, "pag_app/data_vis.html", context)
