import pandas as pd
import folium
from folium.plugins import MarkerCluster

# csvからのデータ読み込み(必要なカラムだけを抽出)
df1 = pd.read_csv(
    './data/ame_master_20230824.csv',
    usecols=['観測所番号','種類','観測所名','所在地','緯度(度)','緯度(分)','経度(度)','経度(分)','海面上の高さ(ｍ)'],
    encoding='cp932'
    )
df2 = pd.read_csv(
    './data/ame_master_20230824.csv',
    usecols=['観測所番号','種類','観測所名','所在地','緯度(度)','緯度(分)','経度(度)','経度(分)','海面上の高さ(ｍ)'],
    encoding='cp932'
    )

df = pd.concat([df1, df2])

df['緯度(10進)'] = df['緯度(度)'] + df['緯度(分)'] / 60
df['経度(10進)'] = df['経度(度)'] + df['経度(分)'] / 60

# 地図生成（東京千代田区北の丸公園：東京管区気象台 中心）
folium_map = folium.Map(location=[35.691666, 135.751666], zoom_start=14)
marker_cluster = MarkerCluster().add_to(folium_map)

# マーカープロット
for i, row in df.iterrows():
    count = row['種類']
    if count == '官':  # 気象官署
        folium.Marker(
            location=[row['緯度(10進)'], row['経度(10進)']],
            popup=row['観測所名'],
            icon=folium.Icon(color='red')
        ).add_to(marker_cluster)
    elif count == '四':  # 四要素観測所
        folium.Marker(
            location=[row['緯度(10進)'], row['経度(10進)']],
            popup=row['観測所名'],
            icon=folium.Icon(color='orange')
        ).add_to(marker_cluster)
    elif count == '三':  # 三要素観測所
        folium.Marker(
            location=[row['緯度(10進)'], row['経度(10進)']],
            popup=row['観測所名'],
            icon=folium.Icon(color='lightgreen')
        ).add_to(marker_cluster)
    elif count == '雨':  # 雨量観測所
        folium.Marker(
            location=[row['緯度(10進)'], row['経度(10進)']],
            popup=row['観測所名'],
            icon=folium.Icon(color='blue')
        ).add_to(marker_cluster)
    else:  # 積雪観測所
        folium.Marker(
            location=[row['緯度(10進)'], row['経度(10進)']],
            popup=row['観測所名'],
            icon=folium.Icon(color='gray')
        ).add_to(marker_cluster)

# 地図表示
folium_map.save('./data/amedas-map.html')
