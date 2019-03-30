
import sqlite3
import pandas as pd
import folium

conn = sqlite3.connect('./a4-sampled.db')
c = conn.cursor()

strt_year = int(input("Enter start year (YYYY):"))
end_year = int(input("Enter end_year (YYYY):"))
number_nbhd = int(input("Enter number of neighbourhoods:"))

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

result1 = crimes.iloc[0:number_nbhd, 1:]
result2 = crimes.iloc[0:number_nbhd, 0]
result = pd.concat([result1, result2], axis =1)

#print(result.to_string(index = False))
#print(result)

parent = '''SELECT neighbourhood_name,crime_type, sum(incidents_count) as total_incidents  from crime_incidents
where year between %d and %d
group by neighbourhood_name, crime_type 
order by neighbourhood_name asc, total_incidents desc''' % (strt_year, end_year)

p_test = pd.read_sql_query(parent,conn)
dummy = p_test.groupby("Neighbourhood_Name").head(1)
#print(dummy)
conn.close()
#print(result)
test1 = pd.merge(result, dummy, on = 'Neighbourhood_Name')
print(test1)
'''
select neighbourhood_name, crime_type, sum(incidents_count) as total
from crime_incidents
where crime_type in (select crime_type from crime_incidents
group by crime_type
having max(incidents_count))
and neighbourhood_name = 'ALLENDALE'
group by neighbourhood_name, crime_type
limit 25;
'''
#hell0s