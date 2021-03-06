import os
import random
import datetime
import matplotlib.pyplot as plt

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from Plot import Plot as Plot
from climatology import Climatology as Climatology
from regions import Plot as regionPlot
from regions import Climatology as regionClimatology
from regions import AllData as AllData
import allData

from django import template

from regionDicts import *

import django
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

def testing(request):
    errors = []
    return render_to_response('main.html',
        {'errors': errors,})

def bargraph_panel(request):
    try:
        data = [1,2,3,4,5]
        variableList = ["", "mdn","pon","spi","spei","pdsi","pzi", "scpdsi"]
        if 'run_avg' in request.GET:
            run_avg = request.GET['run_avg']
            if not run_avg:
                runAvg = 0
            else:
                runAvg = int(run_avg)

        if 'lat' in request.GET:
            lat = request.GET['lat']
            if not lat:
                lat = 40
            else:
                lat = float(lat)

        if 'lon' in request.GET:
            lon = request.GET['lon']
            if not lon:
                lon = -100
            else:
                lon = float(lon)

        if 'start_year' in request.GET:
            startYear = request.GET['start_year']
            if startYear < 1895:
                startYear = 1895
            else:
                startYear = int(startYear)

        if 'end_year' in request.GET:
            endYear = request.GET['end_year']
            endYear = int(endYear)
            #if endYear > datetime.datetime.now().year:
            #    endYear = (datetime.datetime.now().year -1)
            #else:
            #    endYear = int(endYear)

        #if 'variable' in request.GET:
        #    variable = int(request.GET['variable'])
        #    variable = variableList[variable]

      
        variable = int(request.GET['variable'])
        variable = variableList[variable]
        month = int(request.GET['month'])
        span = int(request.GET['span'])
   
        # Print PNG to page
        try:
            newPlot = Plot(lat=lat, lon=lon, startYear=startYear, endYear=endYear, variable=variable, month=month, span=span, runavg=runAvg, data=None)
            fig = newPlot.getData()            

            canvas=FigureCanvas(fig)
            response=django.http.HttpResponse(content_type='image/png')
            canvas.print_png(response)

            return response
        except:
            return HttpResponse("Plot feature under development for this location.")
    except:
        return HttpResponse("No data.")

def regionsBargraph_panel(request):
    try:
        data = [1,2,3,4,5]
        variableList = ["", "mdn","pon","spi", 'spei',"pdsi","pzi", "scpdsi"]
        if 'run_avg' in request.GET:
            run_avg = request.GET['run_avg']
            if not run_avg:
                runAvg = 0
            else:
                runAvg = int(run_avg)

        region = request.GET['region']
        #print region
 

        if 'start_year' in request.GET:
            startYear = request.GET['start_year']
            if startYear < 1895:
                startYear = 1895
            else:
                startYear = int(startYear)

        if 'end_year' in request.GET:
            endYear = request.GET['end_year']
            endYear = int(endYear)
            #if endYear > datetime.datetime.now().year:
            #    endYear = (datetime.datetime.now().year -1)
            #else:
            #    endYear = int(endYear)

        #if 'variable' in request.GET:
        #    variable = int(request.GET['variable'])
        #    variable = variableList[variable]

      
        variable = int(request.GET['variable'])
        variable = variableList[variable]
        month = int(request.GET['month'])
        span = int(request.GET['span'])
   
        # Print PNG to page
        try:
            newPlot = regionPlot(region=region, startYear=startYear, endYear=endYear, variable=variable, month=month, span=span, runavg=runAvg, data=None)
            fig = newPlot.getData()            

            canvas=FigureCanvas(fig)
            response=django.http.HttpResponse(content_type='image/png')
            canvas.print_png(response)

            return response
        except:
            return HttpResponse("Plot feature under development for this location.")
    except:
        return HttpResponse("No data.")




def bargraph_text(request):
    variableList = ["", "mdn","pon","spi","spei","pdsi","pzi", "scpdsi"]
    if 'run_avg' in request.GET:
        run_avg = request.GET['run_avg']
        if not run_avg:
            runAvg = 0
        else:
            runAvg = int(run_avg)
  
    lat = float(request.GET['lat'])
    lon = float(request.GET['lon'])
    endYear = int(request.GET['end_year'])
    startYear = int(request.GET['start_year'])

    variable = int(request.GET['variable'])
    variable = variableList[variable]
    month = int(request.GET['month'])
    span = int(request.GET['span'])
    text = Plot(lat=lat, lon=lon, startYear=startYear, endYear=endYear, variable=variable, month=month, span=span, runavg=runAvg, data=None).getText()
    data = []
    for value in text:
        data.append(value)
    return render_to_response('print.html', {'data': data})#, {'year': data}, {'mean': data})


def regionBargraph_text(request):
    variableList = ["", "mdn","pon","spi", "spei","pdsi","pzi", "scpdsi"]
    if 'run_avg' in request.GET:
        run_avg = request.GET['run_avg']
        if not run_avg:
            runAvg = 0
        else:
            runAvg = int(run_avg)

    region = request.GET['region']
    endYear = int(request.GET['end_year'])
    startYear = int(request.GET['start_year'])

    variable = int(request.GET['variable'])
    variable = variableList[variable]
    month = int(request.GET['month'])
    span = int(request.GET['span'])
    text = regionPlot(region=region, startYear=startYear, endYear=endYear, variable=variable, month=month, span=span, runavg=runAvg, data=None).getText()
    data = []
    for value in text:
        data.append(value)
    return render_to_response('print.html', {'data': data})#, {'year': data}, {'mean': data})



def all_text(request):
    variableList = ["", "mdn","pon","spi", "spei","pdsi","pzi", "scpdsi"]
  
    lat = float(request.GET['lat'])
    lon = float(request.GET['lon'])
    variable = int(request.GET['variable'])
    variable = variableList[variable]
    text = allData.getAll(lat=lat, lon=lon, variable=variable)

    # Assign Data information
    if variable == "mdn": data = ['Temperature (Degrees F) Mean Departure from Normal']
    if variable == "pon": data = ['Precipitation (Inches)']
    if variable == "spi": data = ['Standardized Precipitaion Index']
    if variable == "spei": data = [' Standardized Evapotranspiration Index']
    if variable == "pdsi": data = ['Palmer Drought Severity Index']
    if variable == "pzi": data = ['Palmer Z-Index']
    if variable == "scpdsi": data = ['Self Calibrated Palmer Drought Severity Index']

    # Set 
    data = data+['%4.2f N, %4.2f W'%(abs(lat),abs(lon)),'________________________________________________________________________________']
    data = data+['Year, Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec']
    for value in text:
        # Send Data as a srting to Django

        dataString = '%4.0f,%4.2f,%4.2f,%4.2f,%4.2f,%4.2f,%4.2f,%4.2f,%4.2f,%4.2f,%4.2f,%4.2f,%4.2f' % (value[0],value[1],value[2],value[3],value[4],value[5],value[6],value[7],value[8],value[9],value[10],value[11],value[12])
        data.append(dataString)


    return render_to_response('print.html', {'data': data})

def regionsAll_text(request):
    variableList = ["", "mdn","pon","spi", "spei","pdsi","pzi", "scpdsi"]
  

    region = request.GET['region']
    variable = int(request.GET['variable'])
    variable = variableList[variable]
    text = AllData(region=region, variable=variable).getAll()

    regionName = allRegionDict[int(region)]

    # add climate division to name if needed
    if int(region) in divDict:
        regionName = regionName + " Climate Division"


    # Assign Data information
    if variable == "mdn": data = ['Temperature (Degrees F)']
    if variable == "pon": data = ['Precipitation (Inches)']
    if variable == "spi": data = ['Standardized Precipitaion Index']
    if variable == "spei": data = ['Standardized Evapotranspiration Index']
    if variable == "pdsi": data = ['Palmer Drought Severity Index']
    if variable == "pzi": data = ['Palmer Z-Index']
    if variable == "scpdsi": data = ['Self Calibrated Palmer Drought Severity Index']

    # Set 
    data = data+[regionName,'________________________________________________________________________________']
    data = data+['Year, Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec']
    for value in text:
        # Send Data as a srting to Django

        dataString = '%4.0f,%4.2f,%4.2f,%4.2f,%4.2f,%4.2f,%4.2f,%4.2f,%4.2f,%4.2f,%4.2f,%4.2f,%4.2f' % (value[0],value[1],value[2],value[3],value[4],value[5],value[6],value[7],value[8],value[9],value[10],value[11],value[12])
        data.append(dataString)


    return render_to_response('print.html', {'data': data})


def wait_message(request):
    return render_to_response('wait.html')
    

def climatology(request):
    try:
        data = [1,2,3,4,5]
        variableList = ["", "mdn","pon","spi", "spei", "pdsi","pzi", "scpdsi"]

        if 'lat' in request.GET:
            lat = request.GET['lat']
            if not lat:
                lat = 40
            else:
                lat = float(lat)

        if 'lon' in request.GET:
            lon = request.GET['lon']
            if not lon:
                lon = -100
            else:
                lon = float(lon)

      
        variable = int(request.GET['variable'])
        variable = variableList[variable]

        monthSpan = int(request.GET['span'])
        year = int(request.GET['year'])
        month = int(request.GET['month'])

   
        # Print PNG to page
        try:
            newPlot = Climatology(lat=lat, lon=lon, variable=variable, monthSpan=monthSpan, month=month, year=year)
            fig = newPlot.getData()            

            canvas=FigureCanvas(fig)
            response=django.http.HttpResponse(content_type='image/png')
            canvas.print_png(response)

            return response
        except:
            return HttpResponse("Plot feature under development for this location.")
    except:
        return HttpResponse("No data.")

def climatology_text(request):
    variableList = ["", "mdn","pon","spi", "spei", "pdsi","pzi", "scpdsi"]
    if 'lat' in request.GET:
        lat = request.GET['lat']
        if not lat:
            lat = 40
        else:
            lat = float(lat)

    if 'lon' in request.GET:
        lon = request.GET['lon']
        if not lon:
            lon = -100
        else:
            lon = float(lon)
      
    variable = int(request.GET['variable'])
    variable = variableList[variable]
    #print 'variable:', variable
    monthSpan = int(request.GET['span'])

    year = int(request.GET['year'])
    month = int(request.GET['month'])
   
    text = Climatology(lat=lat, lon=lon, variable=variable, monthSpan=monthSpan, month=month, year=year).getText()
    #print 'text:', text[:]
    data = []
    for value in text:
        data.append(value)
    return render_to_response('print.html', {'data': data})#, {'year': data}, {'mean': data})

def climatologyRegions(request):
    try:
        data = [1,2,3,4,5]
        variableList = ["", "mdn","pon","spi", "spei","pdsi","pzi", "scpdsi"]

        region = request.GET['region']


      
        variable = int(request.GET['variable'])
        variable = variableList[variable]

        monthSpan = int(request.GET['span'])

        year = int(request.GET['year'])
        month = int(request.GET['month'])
   
        # Print PNG to page
        try:
            newPlot = regionClimatology(region=region, variable=variable, monthSpan=monthSpan, month=month, year=year)
            fig = newPlot.getData()            

            canvas=FigureCanvas(fig)
            response=django.http.HttpResponse(content_type='image/png')
            canvas.print_png(response)

            return response
        except:
            return HttpResponse("Plot feature under development for this location.")
    except:
        return HttpResponse("No data.")

def climatologyRegions_text(request):
    variableList = ["", "mdn","pon","spi","spei","pdsi","pzi", "scpdsi"]

    region = request.GET['region']
      
    variable = int(request.GET['variable'])
    variable = variableList[variable]
    #print 'variable:', variable
    monthSpan = int(request.GET['span'])
    year = int(request.GET['year'])
    month = int(request.GET['month'])
   
    text = regionClimatology(region=region, variable=variable, monthSpan=monthSpan, month=month, year=year).getText()
    #print 'text:', text[:]
    data = []
    for value in text:
        data.append(value)
    return render_to_response('print.html', {'data': data})#, {'year': data}, {'mean': data})
