import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import folium
def q2():
    conn = sqlite3.connect("a4-sampled.db")
    c = conn.cursor()
    n_value = int(input("Enter number of locations:"))
    m = folium.Map(location=[53.5444,-113.323], zoom_start=11)
    sql_top_bot = '''
            SELECT *
            FROM (SELECT p.Neighbourhood_Name, c.Latitude, c.Longitude, (CANADIAN_CITIZEN+NON_CANADIAN_CITIZEN+NO_RESPONSE) as Total
            FROM population p, coordinates c
            WHERE p.Neighbourhood_name = c.Neighbourhood_name and total > 0 and c.Latitude != 0 and c.Longitude != 0
            ORDER BY Total DESC LIMIT {})
            UNION
            SELECT *
            FROM (SELECT p.Neighbourhood_Name, c.Latitude, c.Longitude, (CANADIAN_CITIZEN+NON_CANADIAN_CITIZEN+NO_RESPONSE) as Total
            FROM population p, coordinates c
            WHERE p.Neighbourhood_name = c.Neighbourhood_name and total > 0 and c.Latitude != 0 and c.Longitude != 0
            ORDER BY Total ASC LIMIT {})
            ORDER BY Total
        '''.format(n_value, n_value)
    data = pd.read_sql_query(sql_top_bot,conn)
    for i in range(n_value):
        folium.Circle(
            location=[data.iloc[i]['Latitude'], data.iloc[i]['Longitude']],
            popup=data.iloc[i]['Neighbourhood_Name'] + '\n' + str(data.iloc[i]['Total']),
            radius = int(data.iloc[i]['Total']) * 1.1,
            color = 'green',
            fill = True,
            fill_color='darkgreen',
        ).add_to(m)
    for i in range(n_value,len(data)):
        folium.Circle(
            location=[data.iloc[i]['Latitude'], data.iloc[i]['Longitude']],
            popup=data.iloc[i]['Neighbourhood_Name'] + '\n' + str(data.iloc[i]['Total']),
            radius = int(data.iloc[i]['Total']) * 0.1,
            color = 'crimson',
            fill = True,
            fill_color='red',
        ).add_to(m)
    m.save('q2.html')


    #https://www.programcreek.com/python/example/101334/pandas.read_sql_query
    conn.close()
q2()