import requests
import pandas as pd
import json
import time
from datetime import datetime, timedelta

urls = [
    'https://services5.arcgis.com/SaBe5HMtmnbqSWlu/arcgis/rest/services/VIEW_RussiaCoTinUkraine_V3/FeatureServer/49?f=json',
    'https://services5.arcgis.com/SaBe5HMtmnbqSWlu/arcgis/rest/services/VIEW_ClaimedRussianTerritoryinUkraine_V2/FeatureServer/49?f=json',
    'https://services5.arcgis.com/SaBe5HMtmnbqSWlu/arcgis/rest/services/VIEW_Russian_controlled_Ukrainian_Territory_before_February_24_2022/FeatureServer/36?f=json',
    'https://services5.arcgis.com/SaBe5HMtmnbqSWlu/arcgis/rest/services/MDS_AssessedRussianAdvanceInUkraine_view/FeatureServer/49?f=json',
    'https://services5.arcgis.com/SaBe5HMtmnbqSWlu/arcgis/rest/services/VIEW_ClaimedUkrainianCounteroffensives_V2/FeatureServer/51?f=json',
    'https://services5.arcgis.com/SaBe5HMtmnbqSWlu/arcgis/rest/services/VIEW_Reported_Ukrainian_Partisan_Warfare_V2/FeatureServer/53?f=json'
]

list_ = []
for url in urls:
    dic = {}
    data = requests.get(url).json()
    dic['name'] = data['name']
    dic['lastEditDate'] = data['editingInfo']['lastEditDate']
    list_.append(dic)
    time.sleep(1)

df = pd.DataFrame(list_)

df.lastEditDate = pd.to_datetime(df.lastEditDate,unit='ms')

df.to_csv('./data/'+(datetime.today() - timedelta(days=1)).strftime(format='%Y%m%d')+'_'+'lastEditDate.csv',index=False)

layer = pd.DataFrame(requests.get(
    'https://www.arcgis.com/sharing/rest/content/items/9f04944a2fe84edab9da31750c2b15eb/data?f=json'
).json()['operationalLayers'])

layer['layer'] = layer.url.str.extract('services/(.*)/FeatureServer')

query = '/query?f=geoJSON&maxRecordCountFactor=4&resultOffset=0&resultRecordCount=8000&where=1%3D1&orderByFields=OBJECTID&outFields=OBJECTID&resultType=tile&spatialRel=esriSpatialRelIntersects&geometryType=esriGeometryEnvelope&defaultSR=102100'

for i in range(len(layer)):
    data = requests.get(layer.url[i]+query).json()
    json_string = json.dumps(data)
    with open('./data/'+(datetime.today() - timedelta(days=1)).strftime(format='%Y%m%d')+'_'+layer.layer[i]+'.geojson', 'w') as f:
        f.write(json_string)
    time.sleep(5)




