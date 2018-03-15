# -*- coding: utf-8 -*-

import os
from settings import *
Subway_Map = {}
name_to_id = {}
id_to_name = {}
id_to_line = {}

def dij_findnode(cost, visited):
    minDist = 99999
    node = None
    for i in Subway_Map.keys():
        if (cost[i] < minDist) and (i not in visited):
            minDist = cost[i]
            node = i
    return node

def get_path(parents, start, end):
    path = []
    print_path(parents, start, end, path)
    return path

def print_path(parents, start, end, path):
    if end == start:
        #print id_to_name[start]
        path.append(start)
    else:
        print_path(parents, start, parents[end], path)
        #print id_to_name[end]
        path.append(end)

def dijkstra(start_name, end_name, flag):
    cost = {}
    parents = {}
    visited = []

    start = name_to_id[start_name]
    visited.append(start)
    station_num = len(Subway_Map)
    for i in range(station_num):
        cost[i] = 99999
    for i in Subway_Map[int(start)].keys():
        if(flag == 1):
            cost[i] = Subway_Map[start][i]
        else:
            cost[i] = 1
        parents[i] = start

    node = dij_findnode(cost, visited)
    while node is not None:
        for i in Subway_Map[node]:  # 所有node结点的邻居结点
            if flag == 1:
                newcost = cost[node] + Subway_Map[node][i]
            elif flag == 2:
                newcost = cost[node] + 1
            else:
                if parents[node] is not None:
                    a = list(set(id_to_line[parents[node]]).intersection(set(id_to_line[node])))
                    b = list(set(id_to_line[node]).intersection(set(id_to_line[i])))
                    if a != b:
                        newcost = cost[node] + 99
                    else:
                        newcost = cost[node] + 1
                else:
                    newcost = cost[node] + 1
            if newcost < cost[i]:
                parents[i] = node
                cost[i] = newcost
        visited.append(node)
        node = dij_findnode(cost, visited)
    end = name_to_id[end_name]

    path = get_path(parents, start, end)
    #for i in range(len(path)):
     #   print id_to_name[path[i]]
    return create_data(path)

def create_data(path):
    data = {}
    station_num = len(path)
    total_distance = 0
    trans_num = 0
    line_name = []
    path_name = []
    for i in range(len(path)):
        path_name.append(id_to_name[path[i]])

    for i in range(station_num - 1):
        total_distance = total_distance + Subway_Map[path[i]][path[i + 1]]
    for i in range(station_num):
        if len(id_to_line[path[i]]) == 1:
            line_name.append(id_to_line[path[i]][0])
        else:
            if i == 0:
                line_union = set(id_to_line[path[i + 1]]).intersection(set(id_to_line[path[i]]))
                line_name.append(list(line_union)[0])
            else:
                line_union = set(id_to_line[path[i - 1]]).intersection(set(id_to_line[path[i]]))
                line_name.append(list(line_union)[0])

    trans_num = len(set(line_name))

    route = []
    start = 0
    end = 0
    for i in range(1, station_num):
        if line_name[i] != line_name[i - 1]:
            end = i - 1
            route_data = {}
            route_data['line'] = line_name[i - 1]
            route_data['start'] = path_name[start]
            route_data['station'] = path_name[start:end + 1]
            route_data['end'] = path_name[end]
            route.append(route_data)
            start = end

    end = station_num
    route_data = {}
    route_data['line'] = line_name[end - 1]
    route_data['start'] = path_name[start]
    route_data['station'] = path_name[start:]
    route_data['end'] = path_name[end - 1]
    route.append(route_data)

    data['route'] = route
    data['station_num'] = station_num
    data['trans_num'] = trans_num
    data['total_distance'] = total_distance
    print data
    return data

def create_map():
    data_dir = (STATIC_ROOT.split("collectstatic")[0]+"static/data")
    files = os.listdir(data_dir)

    station_num = -1

    for file in files:

        f = open(STATIC_ROOT.split("collectstatic")[0]+"static/data/"+file, 'r')
        line = f.readline()[:-1]
        line_data = line.split('\t')
        station = line_data[0].split('——')
        #print file[:-4].decode('gbk').encode('utf-8')

        if station[0] not in name_to_id:
            station_num = station_num + 1
            name_to_id[station[0]] = station_num
            id_to_name[station_num] = station[0]

            line_name = []
            if station_num not in id_to_line:
                line_name.append(file[:-4])
                id_to_line[station_num] = line_name
        elif file[:-4] not in id_to_line[name_to_id[station[0]]]:
            id_to_line[name_to_id[station[0]]].append(file[:-4])

        while line:
            distance = int(line_data[1])

            if station[1] not in name_to_id:
                station_num = station_num + 1
                name_to_id[station[1]] = station_num
                id_to_name[station_num] = station[1]
                line_name = []
                if station_num not in id_to_line:
                    line_name.append(file[:-4])
                    id_to_line[station_num] = line_name
            elif file[:-4] not in id_to_line[name_to_id[station[1]]]:
                    id_to_line[name_to_id[station[1]]].append(file[:-4])

            if name_to_id[station[0]] not in Subway_Map:
                adj_dict = {}
                adj_dict[name_to_id[station[1]]] = distance
                Subway_Map[name_to_id[station[0]]] = adj_dict
            else:
                Subway_Map[name_to_id[station[0]]][name_to_id[station[1]]] = distance

            if name_to_id[station[1]] not in Subway_Map:
                adj_dict = {}
                adj_dict[name_to_id[station[0]]] = distance
                Subway_Map[name_to_id[station[1]]] = adj_dict
            else:
                Subway_Map[name_to_id[station[1]]][name_to_id[station[0]]] = distance

            line = f.readline()[:-1]
            line_data = line.split('\t')
            station = line_data[0].split('——')

        '''
        print "______________________"
        for a in Subway_Map:
            print a,Subway_Map[a]
        print "______________________"
        return
        '''
    '''
    print "______________________"
    for a in Subway_Map:
        print a, Subway_Map[a]
    print "______________________"
    '''

def get_shortest_distance(start_name,end_name):
    create_map()
    #for i in range(len(id_to_line)):
    #    print i,id_to_line[i]
    #exit()
    '''
    start_name = raw_input("起始站: ")
    #start_name = "人民大学"
    while start_name not in name_to_id:
        print "起始站不存在，请重新输入"
        start_name = raw_input("起始站: ")

    end_name = raw_input("终点站: ")
    #end_name = "北京站"
    while end_name not in name_to_id:
        print "终点站不存在，请重新输入"
        end_name = raw_input("终点站: ")

    #print "----------最短距离----------"
    '''
    return dijkstra(start_name, end_name, 1)
    '''
    print ""
    print "----------最少站点----------"
    dijkstra(start_name, end_name, 2)
    print ""
    print "----------最少换乘----------"
    dijkstra(start_name, end_name, 3)
    '''

def get_least_station(start_name,end_name):
    create_map()
    # for i in range(len(id_to_line)):
    #    print i,id_to_line[i]
    # exit()
    '''
    start_name = raw_input("起始站: ")
    # start_name = "人民大学"
    while start_name not in name_to_id:
        print "起始站不存在，请重新输入"
        start_name = raw_input("起始站: ")

    end_name = raw_input("终点站: ")
    # end_name = "北京站"
    while end_name not in name_to_id:
        print "终点站不存在，请重新输入"
        end_name = raw_input("终点站: ")
    '''

    #print "----------最短距离----------"
    return dijkstra(start_name, end_name, 2)

def get_least_trans(start_name,end_name):
    create_map()
    # for i in range(len(id_to_line)):
    #    print i,id_to_line[i]
    # exit()
    '''
    start_name = raw_input("起始站: ")
    # start_name = "人民大学"
    while start_name not in name_to_id:
        print "起始站不存在，请重新输入"
        start_name = raw_input("起始站: ")

    end_name = raw_input("终点站: ")
    # end_name = "北京站"
    while end_name not in name_to_id:
        print "终点站不存在，请重新输入"
        end_name = raw_input("终点站: ")
    '''

    #print "----------最短距离----------"
    return  dijkstra(start_name, end_name, 3)

