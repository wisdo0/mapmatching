# from sqlalchemy import create_engine
# engine_pg = create_engine('postgresql://postgres:1234@localhost:5432/postgres')
import psycopg2
import pandas as pd
import osmnx as ox
import numpy as np
# from scipy.spatial.distance import euclidean
# from osmnx import distance
# import osmnx as ox
import networkx as nx
# import pandas as pd
import geopandas as gpd
import geatpy as ea
import transbigdata as tbd
#%%
from pyproj import Transformer
from scipy.spatial.distance import euclidean

transformer = Transformer.from_crs("epsg:4326", "epsg:3857")
class MyProblem(ea.Problem):  # 继承Problem父类
    def __init__(self):
        name = 'MyProblem'  # 初始化name（函数名称，可以随意设置）
        M = 2  # 优化目标个数
        maxormins = [1] * M  # 初始化maxormins（目标最小最大化标记列表，1：最小化该目标；-1：最大化该目标）
        Dim = len(dataf)  # 初始化Dim（决策变量维数）
        varTypes = [1] * Dim  # 初始化varTypes（决策变量的类型，0：实数；1：整数）
        lb = [0] * Dim  # 决策变量下界

        ub = [len(x) for x in dataf['cand']]  # 决策变量上界
        lbin = [1] * Dim  # 决策变量下边界（0表示不包含该变量的下边界，1表示包含）
        ubin = [0] * Dim  # 决策变量上边界（0表示不包含该变量的上边界，1表示包含）
        # 调用父类构造方法完成实例化
        ea.Problem.__init__(self, name, M, maxormins, Dim, varTypes, lb, ub, lbin, ubin)

    def evalVars(self, Vars):  # 目标函数
        #构建路径
        a = [dis(each) for each in Vars]
        ObjV = np.array(a)  # 计算目标函数值矩阵
        # CV =np.array([0] * len(Vars)).T  # 构建违反约束程度矩阵
        # return ObjV, CV
        return ObjV

#
# def axis_conversion(data, lat, lon):
#     #注意lat 在前，lon在后，不能写反
#     lon = data[lon].values
#     lat = data[lat].values
#     # transformer = Transformer.from_crs("epsg:4326", "epsg:3857")
#     #这里将epsg4326转换为epsg3857
#     #关于坐标系的知识可以参考这个网址：https://www.cnblogs.com/E7868A/p/11460865.html
#     x3, y3 = transformer.transform(lat, lon)
#     return (x3,


def dis(Vars):
    id = [cand[each][Vars[each]] for each in range(len(Vars))]
    a = id[:-1]
    b = id[1:]
    length=0
    for each in range(len(a)):
        length+=nx.shortest_path_length(G, a[each], b[each], weight="length")
    # path = ox.shortest_path(G, a, b, weight="length", cpus=None)
    # pathnode = []
    # for each in path:
    #     if each ==None:
    #         return [10**6,10**6]
    #     pathnode.extend(each[:-1])
    # pathnode.append(id[-1])
    # lat = []
    # lon = []
    # length = 0
    # nod = None
    # for each in pathnode:
    #     lat.append([G.nodes[each]['y']])
    #     lon.append([G.nodes[each]['x']])
    #     # print(nod)
    #     # print(each)
    #     if nod:
    #         length += G[nod][each][0]['length']
    #     nod = each
    lat = []
    lon = []
    for each in id:
        lat.append([G.nodes[each]['y']])
        lon.append([G.nodes[each]['x']])
    lat = np.array(lat)
    lon = np.array(lon)
    x1, x2 = transformer.transform(lat, lon)
    x = np.hstack([x1, x2])
    # x = np.hstack([lat, lon])
    y1, y2 = transformer.transform(df['latitude'].values, df['longitude'].values)
    y = np.hstack([y1, y2])
    # y = np.hstack([df['latitude'].values, df['longitude'].values])
    # y = pd.concat([df['latitude'], df['longitude']], axis=1, ignore_index=True)
    # y = y.values
    # y=dataf['id'].values
    # y=[df['latitude'],df['longitude']]
    #计算评价函数
    f, _ = fastdtw(x, y, dist=euclidean)
    return [f, length]
#%%


def get_ids(df, each, dist=50):
    if dist > 200:
        raise ValueError("dist error,index={index}".format(index=each))
    else:
        q = 'SELECT u FROM public.edges where ST_DWithin(ST_Point({x},{y},4326)::geography,geometry::geography,{dist}) order by (ST_Point({x},{y},4326)::geography <-> geometry::geography) limit 10;'.format(
            x=df.loc[each, "longitude"], y=df.loc[each, "latitude"], dist=dist)
        pgisCursor.execute(q)
        idlist = [x[0] for x in pgisCursor.fetchall()]
        if not idlist:
            idlist = get_ids(df, each, dist + 50)
        return idlist


# ox.config(overpass_settings='[out:json][timeout:90][date:"2014-02-01T19:20:00Z"]')
# place ="Roma Capitale"
# G = ox.graph_from_place(place, network_type='drive_service')
# ox.save_graphml(G,'rome.graphml')

# filepath = "rome.graphml"
# G = ox.load_graphml(filepath)

# nodes, edges = ox.graph_to_gdfs(G, nodes=True, edges=True)
pgisCon = psycopg2.connect(database="postgres", user="postgres", password="1234")
pgisCursor = pgisCon.cursor()
# pd.set_option('precision', 14)
# df = pd.read_csv(r"D:\data\rome_new\0.csv", float_precision='high')
df = pd.read_csv(r"rome_final.csv", float_precision='high')
df = df[df['tag_new'] == 15].copy().reset_index(drop=True)
#%%
data = []
outoflimit = []
for each in df.index:
    try:
        data.append([each, get_ids(df, each)])
    except ValueError:
        outoflimit.append(each)
# data.columns = ['index', 'cand']
dataf = pd.DataFrame(data, columns=['index', 'cand'])
cand = dataf['cand'].tolist()
# dataf.to_csv('dataf.csv',index=0)
pgisCon.close()
# df=pd.read_csv('rome1.csv')
west = 12.2019
east = 12.8416
south = 41.6456
north = 42.1089
# west=df['longitude'].min()
# east=df['longitude'].max()
# south=df['latitude'].min()
# north=df['latitude'].max()
ox.settings.overpass_settings = '[out:json][timeout:90][date:"2014-02-01T19:20:00Z"]'
# place ="Roma Capitale"
# 41.6456,12.2019 : 42.1089,12.8416
G = ox.graph_from_bbox(north, south, east, west, network_type='drive_service')
from fastdtw import fastdtw
#%%





# 实例化问题对象
problem = MyProblem()
# 构建算法
algorithm = ea.moea_NSGA2_templet(problem,
                                  ea.Population(Encoding='RI', NIND=10),
                                  MAXGEN=50,  # 最大进化代数
                                  logTras=20)  # 表示每隔多少代记录一次日志信息，0表示不记录。
# 求解
res = ea.optimize(algorithm, seed=1, verbose=False, drawing=1, outputMsg=True, drawLog=False, saveFlag=False,
                  dirName='result')