# -*- coding: utf-8 -*-

# from django.http import HttpResponse
from django.shortcuts import render
import json
from django.http import HttpResponse
from index import *
from django.views.decorators.csrf import csrf_exempt


def index(request):
    context = {}
    return render(request, 'index.html', context)

@csrf_exempt
def get_result(request):
    context = {}
    color_dict = {'地铁一号线': '#fbebea', '地铁二号线': '#e6eff6', '地铁四号线': '#dff5f2', '地铁十号线': '#e3f3f6',
                  '地铁五号线': '#f8eaf3', '地铁六号线': '#fbf1df', '地铁七号线': '#f4eee7', '地铁八号线': '#e4f4e5',
                  '地铁九号线': '#edf3e0','地铁13号线': '#f5ecde', '地铁14号线(东)': '#f4eceb', '地铁14号线(西)': '#f4eceb',
                  '地铁15号线': '#edeaf3', '地铁16号线': '#e7eeea','地铁八通线': '#fbebea','地铁昌平线': '#f3edf0',
                  '地铁亦庄线': '#fae7eb', '地铁房山线': '#f9ece3', '机场线': '#f3f0f4'}

    p_from = request.POST['from'].encode('utf-8')
    p_to = request.POST['to'].encode('utf-8')
    '''
    context['hello'] = 'Hello World!'

    context['data'] = {'route':[{	'line':'地铁一号线','start':'人民大学','station':['魏公村','动物园'],'end':'西直门','station_num':2},
                        {'line':'地铁五号线','start':'西直门','station':['复兴门','前门','崇文门'],'end':'北京站','station_num':3},],
               'station_num':22,
               'trans_num':1,
               'total_distance':2000,
    }
    '''

    context['gsd'] = get_shortest_distance(p_from,p_to)
    for route in context['gsd']['route']:
        route['color'] = color_dict[route['line']]

    context['gls'] = get_least_station(p_from,p_to)
    for route in context['gls']['route']:
        route['color'] = color_dict[route['line']]

    context['glt'] = get_least_trans(p_from,p_to)
    for route in context['glt']['route']:
        route['color'] = color_dict[route['line']]
    context['status'] = 1
    resp = HttpResponse(json.dumps(context), content_type="application/json")
    return resp

get_shortest_distance('人民大学','西单')



    #return render(request, 'index.html', context)
