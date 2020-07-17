from pyecharts.charts import Map,Pie,Radar
from pyecharts import options as opts
from namemap import nameMap
import json
import requests
import random
#从api调取数据并存储
url1 = 'https://api.inews.qq.com/newsqa/v1/automation/foreign/country/ranklist'
url2='https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
data_1=requests.get(url1).json()
data_2 = requests.get(url2).json()['data']
all = json.loads(data_2)

#创建列表和字典
name=[]#国家名
confirm=[]#确诊人数
dead=[]#死亡人数
heal=[]#治愈人数
nameMap_new={}
names_new=[]
ds={}#死亡人数字典
hs={}#治愈人数字典

#向列表添加元素
for a_dict in data_1['data']:
    name.append(a_dict['name'])
    confirm.append(a_dict['confirm'])
    dead.append(a_dict['dead'])
    heal.append(a_dict['heal'])
    #如果死亡人数>5000，则更新死亡人数字典
    if a_dict['dead'] is not None and a_dict['name'] is not None:
        if int(a_dict['dead']) > 5000:
            d = {a_dict['name']:a_dict['dead']}
            h = {a_dict['name']:a_dict['heal']}
            ds.update(d)
            hs.update(h)
ds = dict(sorted(ds.items(), key = lambda k: k[1]))#根据字典中值的大小，对字典中的项排序
hs = dict(sorted(hs.items(), key = lambda k: k[1]))
country_list = ds.keys()
dead_list = ds.values()
heal_list = hs.values()

#键值互换
for a,b in nameMap.items():
    nameMap_new[b]=a

#中英文国名映射
for i in range(len(name)):
    name_new=nameMap_new[name[i]]
    names_new.append(name_new)

#添加中国数据
chinaTotal=all['chinaTotal']
confirm.append(chinaTotal['confirm'])
dead.append(chinaTotal['dead'])
heal.append(chinaTotal['heal'])
names_new.append('China')

#随机配色
def randomcolor(lenth):
    colors = []
    for i in range(lenth):
        color_ = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
        color = ""
        for i in range(6):
            color += color_[random.randint(0, 14)]#生成一个指定范围内的整数
        colors.append("#" + color)
    return colors
color_matching = randomcolor(len(dead_list))


def  Cartography():

    #创建地图
    map = Map( init_opts=opts.InitOpts(width="1900px", height="900px", bg_color="#d0effa", page_title="全球新冠疫情_1"))
    map.add("确诊人数",[list(z) for z in zip(names_new, confirm)],is_map_symbol_show=False,
            maptype="world",label_opts=opts.LabelOpts(is_show=False),itemstyle_opts=opts.ItemStyleOpts(color="rgb(98,121,146)"))#地图区域颜色
    map.set_global_opts(title_opts = opts.TitleOpts(title='全球新冠疫情确诊人数'),legend_opts=opts.LegendOpts(is_show=False),
                     visualmap_opts=opts.VisualMapOpts(max_=2000000, is_piecewise=True,
                                      pieces=[
                                        {"max": 3000000,"min": 500001,"label":">500000","color":"#460303"},
                                        {"max": 500000, "min": 100001, "label": "100001-500000", "color": "#8A0808"},
                                        {"max": 100000, "min": 10001, "label": "10001-100000", "color": "#B40404"},
                                        {"max": 10000, "min": 1001, "label": "1001-10000", "color": "#DF0101"},
                                        {"max": 1000, "min": 101, "label": "101-1000", "color": "#F78181"},
                                        {"max": 100, "min": 1, "label": "1-100", "color": "#F5A9A9"},
                                        {"max": 0, "min": 0, "label": "0", "color": "#fababa"},
                                        ])  
                     )
    map.render('Global_new_crown_epidemic_map.html')

        #创建饼图
    pie = Pie(init_opts=opts.InitOpts(width='1900px', height='900px',page_title="全球新冠疫情_2",bg_color="#fee4e7"))
    # 添加数据
    pie.add("", [list(z) for z in zip(country_list, dead_list)],
            radius=['20%', '100%'],#设置内径外径
            center=['60%', '65%'],
            rosetype='area')#圆心角相同，通过半径展现数据大小#rosetype='radius'圆心角展现数据百分比，半径展现数据大小
    
    # 设置全局配置
    pie.set_global_opts(title_opts=opts.TitleOpts(title='全球新冠疫情',subtitle='死亡人数超过\n5000的国家\n  (除中国)',
                                               title_textstyle_opts=opts.TextStyleOpts(font_size=15,color= '#f40909'),
                                               subtitle_textstyle_opts= opts.TextStyleOpts(font_size=15,color= '#8a0b0b'),
                                               pos_right= 'center',pos_left= '57%',pos_top= '60%',pos_bottom='center'),
                                legend_opts=opts.LegendOpts(is_show=False))
    # 设置系列配置和颜色
    pie.set_series_opts(label_opts=opts.LabelOpts(is_show=True, position='inside', font_size=13,
                                              formatter='{b}：{c}', font_style='italic',
                                              font_family='Microsoft YaHei'))
    pie.set_colors(color_matching)
    pie.render('Global_new_crown_epidemic_Rose.html')

    #创建雷达图
    radar = Radar(init_opts=opts.InitOpts(width='1900px',height='900px',page_title="全球新冠疫情_3",bg_color="#d1eff3"))
    #由于雷达图传入的数据得为多维数据，所以这里需要做一下处理
    radar_data1 = [list(dead_list)]
    radar_data2 = [list(heal_list)]
    radar.add_schema(
            schema=[
                opts.RadarIndicatorItem(name='巴西', max_=8000),
                opts.RadarIndicatorItem(name='荷兰', max_=8000),
                opts.RadarIndicatorItem(name='伊朗', max_=20000),
                opts.RadarIndicatorItem(name='德国', max_=40000),
                opts.RadarIndicatorItem(name='比利时', max_=70000),
                opts.RadarIndicatorItem(name='英国', max_=80000),
                opts.RadarIndicatorItem(name='法国 ', max_=110000),
                opts.RadarIndicatorItem(name='西班牙', max_=150000),
                opts.RadarIndicatorItem(name='意大利', max_=170000),
                opts.RadarIndicatorItem(name='美国', max_=220000),
            ]
        )
    radar.add("死亡人数",radar_data1,color='blue',areastyle_opts = opts.AreaStyleOpts(opacity = 0.2,color='blue'))
    radar.add("治愈人数",radar_data2,color='red',areastyle_opts=opts.AreaStyleOpts(opacity=0.3,color='red'))
    radar.set_series_opts(label_opts=opts.LabelOpts(is_show=True))
    radar.set_global_opts(title_opts=opts.TitleOpts(title="死亡人数与治愈人数对比")) 
    radar.render("Death_Versus_Heal.html")

Cartography()

