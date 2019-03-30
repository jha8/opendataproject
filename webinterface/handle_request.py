from flask import Flask, request, render_template
import sqlite3
import pandas as pd
import folium

def startup():

    try:
        name = input("Name of the database you will use")
        check_connection = 'file:{}.db?mode=rw'.format(name)
        conn = sqlite3.connect(check_connection, uri=True)
        database_name = "./{}.db".format(name)
        print("Starting up!")
        global dbname
        dbname = database_name
        if __name__ == '__main__':
            app.run(debug=False)

    except sqlite3.OperationalError:
        #If database DNE print out error
        print("database doesn't exist")
        exit(0)



app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/query2')
def query2():
    return render_template('query2.html')

@app.route('/query3')
def query3():
    return render_template('query3.html')

@app.route('/query4')
def query4():
    return render_template('query4.html')









@app.route('/query2', methods = ['GET', 'POST'])
def q2():
    if request.method == 'POST':
        conn = sqlite3.connect(dbname)
        c = conn.cursor()
        n_value = int(request.form["number"])
        m = folium.Map(location=[53.5444, -113.323], zoom_start=11)
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
        m.save('templates/q2.html')
        conn.close()
        return render_template('q2.html')

    #https://www.programcreek.com/python/example/101334/pandas.read_sql_query

@app.route('/query3', methods = ['GET', 'POST'])
def getting_data():
    if request.method == 'POST':
        strt_year = int(request.form["start_year"])
        end_year = int(request.form["end_year"])
        number_nbhd = int(request.form["number"])
        crime_type = request.form["type"]

        conn = sqlite3.connect(dbname)
        c = conn.cursor()

        sql_statement = '''SELECT neighbourhood_name, sum(incidents_count) as total_incidents  from crime_incidents
        where crime_type = '%s'
        and year between %d and %d
        group by neighbourhood_name
        order by incidents_count desc limit %d''' % (crime_type, strt_year, end_year, number_nbhd)

        rows = pd.read_sql_query(sql_statement, conn)

        universe = pd.read_sql_query('''Select * from coordinates''', conn)
        resulting = pd.merge(rows, universe, on='Neighbourhood_Name')
        #
        mapped = folium.Map(location=[resulting['Latitude'].mean(), resulting['Longitude'].mean()], zoom_start=14)

        for row in resulting.head().itertuples():
            folium.Circle(
                location=[row.Latitude, row.Longitude],
                popup="{} <br> {} ".format(row.Neighbourhood_Name, row.total_incidents),
                radius=(30 * (row.total_incidents // 50)),
                color='crimson',
                fill=True,
                fill_color='crimson'
            ).add_to(mapped)

        mapped.save(outfile='templates/q3.html')
        conn.close()
        return render_template('q3.html')


@app.route('/query4', methods = ['GET', 'POST'])
def q4():
    if request.method == 'POST':
        strt_year = int(request.form["start_year"])
        end_year = int(request.form["end_year"])
        number_nbhd = int(request.form["number"])

        conn = sqlite3.connect(dbname)
        m = folium.Map(location=[53.5444,-113.323], zoom_start=11)
        c = conn.cursor()

        start_statement = '''select neighbourhood_name, (canadian_citizen+ non_canadian_citizen+ no_response) as population_count from population 
        where population_count!=0
        group by neighbourhood_name;'''
        population = pd.read_sql_query(start_statement,conn)

        sql_statement = '''SELECT neighbourhood_name, sum(incidents_count) as total_incidents  from crime_incidents
        where year between %d and %d
        group by neighbourhood_name
        order by incidents_count''' % (strt_year, end_year)

        crimes = pd.read_sql_query(sql_statement, conn)

        crimes = pd.merge(crimes, population, on = 'Neighbourhood_Name')
        crimes['ratio'] = crimes['total_incidents']/crimes['population_count']
        crimes = crimes.sort_values(['ratio'], ascending=[False])
        # print(crimes.to_string(index = False))

        listone = ['Neighbourhood_Name', 'ratio']
        resultfound= crimes[[col for col in listone if col in crimes.columns]]
        resultfound = resultfound.iloc[:number_nbhd, :]



        parent = '''SELECT neighbourhood_name,crime_type, sum(incidents_count) as total_incidents  from crime_incidents
        where year between %d and %d
        group by neighbourhood_name, crime_type
        order by neighbourhood_name asc, total_incidents desc''' % (strt_year, end_year)

        dummy = pd.read_sql_query(parent, conn)
        dummy = dummy.groupby("Neighbourhood_Name").head(1)
        listtwo = ['Neighbourhood_Name', 'Crime_Type', 'ratio']
        dummy = pd.merge(resultfound, dummy, on="Neighbourhood_Name")
        semi_final=dummy[[col for col in listtwo if col in dummy.columns]]

        coordinate_query = '''select * from coordinates'''
        coord = pd.read_sql_query(coordinate_query, conn)
        coord = pd.merge(semi_final, coord, on='Neighbourhood_Name')
        listthree = ['Neighbourhood_Name', 'Crime_Type', 'ratio', 'Latitude', 'Longitude']
        final=coord[[col for col in listthree if col in coord.columns]]
        print(final)
        for row in final.head().itertuples():
            folium.Circle(
                location = [row.Latitude, row.Longitude],
                popup = "{} <br> {} <br> {}".format(row.Neighbourhood_Name, row.Crime_Type, row.ratio),
                radius = (1500*(row.ratio)),
                color = 'crimson',
                fill = True,
                fill_color = 'crimson'
            ).add_to(m)
        m.save('templates/q4.html')
        conn.close()
        return render_template('q4.html')

startup()
