import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import folium
def q2():
    conn = sqlite3.connect("a4-sampled.db")
    c = conn.cursor()
    s_year = int(input("Enter start year (YYYY):"))
    end_year = int(input("Enter end_year (YYYY):"))
    number_neigh = int(input("Enter number of neighbourhoods:"))
    sql_top = '''
        select neighbourhood_name, (canadian_citizen+ non_canadian_citizen+ no_response) as population_count 
        from population, coordinates
        where population_count > 0
        group by neighbourhood_name;
    '''.format(s_year, end_year)
    population = pd.read_sql_query(sql_top,conn)
    print(population)

    """
    #m = folium.Map(location=[53.5444,-113.323], zoom_start=11)
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
    """
    """
    sql_top = '''
        select neighbourhood_name, crime_type, max(incidents_count) as total
        from crime_incidents
        group by neighbourhood_name, crime_type
    """
    """
    data = pd.read_sql_query(sql_top_bot,conn)
    print(data)
    '''
    where crime_type in (select crime_type from crime_incidents
        group by crime_type
        having max(incidents_count))
        and neighbourhood_name = 'ALLENDALE'
        
        limit 25;
    """
    #https://www.programcreek.com/python/example/101334/pandas.read_sql_query
    conn.close()
q2()