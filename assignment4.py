import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import folium

# ================================================================================
# // User inputs and error handling
# ================================================================================
def enter_db_name():
    db_name = input("Enter the name of the database you want to access (without .db): \t")
    return db_name
def main():
    database_name = enter_db_name()
    check_connection = 'file:{}.db?mode=rw'.format(database_name)
    try:
        conn = sqlite3.connect(check_connection, uri=True)
        database_name = "./{}.db".format(database_name)
        main_query(database_name)
    except sqlite3.OperationalError:
        print("database doesn't exist, try again!")
        main()
# ================================================================================
# // Main function
# ================================================================================

def main_query(database_name):
    while True:
        print("""
        1. Q1               2. Q2
        3. Q3               4. Q4
        5. QUIT
        """)
        #Ask user to input a number between 1-5
        #Which further calls the respective function
        choice = input('Choose from above: ')
        if choice == '1':
            print('1 option')
            q1(database_name)
        elif choice == '2':
            print('2 option')
            q2(database_name)
        elif choice == '3':
            print('3 option')
            q3(database_name)
        elif choice == '4':
            print('4 option')
            q4(database_name)
        elif choice == '5':
            exit(0)
        else:
            print('Invalid Input. Try again')
# ================================================================================
# // Q1
# ================================================================================
def q1(database_name):
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    conn.close()
    main_query(database_name)
# ================================================================================
# // Q2
# ================================================================================
def q2(database_name):
    conn = sqlite3.connect(database_name)
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
    conn.close()
    main_query(database_name)
# ================================================================================
# // Q3
# ================================================================================
def q3(database_name):
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    conn.close()
    main_query(database_name)
# ================================================================================
# // Q4
# ================================================================================
def q4(database_name):
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    conn.close()
    main_query(database_name)