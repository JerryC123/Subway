#-*- encoding=utf-8 -*-
import os


Subway_Map = {}
name_to_id = {}
id_to_name = {}
id_to_line = {}
cost = {}
parents = {}
visited = []
'''
def loadData():
    files=['1.txt','13.txt','2.txt','5.txt','8t.txt','cp.txt','fs.txt','yz.txt','10.txt','15.txt','4.txt','8.txt','9.txt','dx.txt','jc.txt']
    lines_data={}
    weights={}
    for filename in files:
        with open('data/%s' % filename,'r') as file:
            line_name=file.readline()[:-1]
            lines_data[line_name]=[]
            for line in file:
                line = line.strip()
                lineAttr = line.split('\t')
                station_name, station_time = lineAttr[0],int(lineAttr[1])
                if station_name not in weights:
                    weights[station_name] = station_time
                lines_data[line_name].append(station_name)
    return lines_data,weights
'''

def dij_findnode(cost):
    minDist = 99999
    node = None
    for i in Subway_Map.keys():
        if (cost[i] < minDist) and (i not in visited):
            minDist = cost[i]
            node = i
    return node

def print_path(i):
    if parents[i]:
        print_path(parents[i])
    print id_to_name[i]

def dijkstra():
    start_name = raw_input("start:")
    start = name_to_id[start_name]
    visited.append(start)
    station_num = len(Subway_Map)
    for i in range(station_num):
        cost[i] = 99999
    for i in Subway_Map[int(start)].keys():
        cost[i] = Subway_Map[start][i]
        parents[i] = start
    node = dij_findnode(cost)

    while node:
        for i in Subway_Map[node]:  # 所有node结点的邻居结点
            newcost = cost[node] + Subway_Map[node][i]
            if newcost < cost[i]:
                parents[i] = node
                cost[i] = newcost
        visited.append(node)
        node = dij_findnode(cost)

    end_name = raw_input("end:")
    end = name_to_id[end_name]
    print cost
    print parents
    return
    print start_name
    print_path(end)


def create_map():
    #datalist = ['1号.txt', '2号.txt', '4号.txt', '5号.txt', '6号.txt', '7号.txt', '8号.txt', '9号.txt', '10号.txt', '13号.txt', '14号东.txt', '14号西.txt', '15号.txt', '16号.txt', '八通.txt', '昌平.txt', '房山.txt', '机场.txt', '亦庄.txt', ]
    data_dir = "data"
    files =  os.listdir(data_dir)

    station_num = -1


    for file in files:
        #file_name = file.decode('gbk').encode('utf-8')
        f = open('data/' + file, 'r')
        line = f.readline()[:-1]
        line_data = line.split('\t')
        station = line_data[0].split('——')
        print file[:-4].decode('gbk').encode('utf-8')

        if station[0] not in name_to_id:
            station_num = station_num + 1
            name_to_id[station[0]] = station_num
            id_to_name[station_num] = station[0]
            id_to_line[station_num] = file[:-4]

        while line:
            distance = int(line_data[1][:-3])

            if station[1] not in name_to_id:
                station_num = station_num + 1
                name_to_id[station[1]] = station_num
                id_to_name[station_num] = station[1]
                id_to_line[station_num] = file[:-4]

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
        #'''
    print "______________________"
    for a in Subway_Map:
        print a, Subway_Map[a]
    print "______________________"
#'''

if __name__ == '__main__':
    create_map()
    dijkstra()