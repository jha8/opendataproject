import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

crime_type = input("Enter a crime type:")

strt_year = int(input("Enter start year (YYYY):"))
end_year = int(input("Enter end_year (YYYY):"))

conn = sqlite3.connect("./dataBase.db")
c = conn.cursor()
c.execute("SELECT Crime_Type, Month, Year, COUNT(incidents_Count) FROM crime_incidents WHERE Crime_Type == crime_type GROUP BY Month, Crime_Type;")
rows = c.fetchall()

df = pd.read_sql_query("SELECT Crime_Type, Month, COUNT(incidents_Count) FROM crime_incidents WHERE Crime_Type == crime_type GROUP BY Month ;", conn)
#query = '''SELECT Crime_Type, Month, COUNT(incidents_Count) FROM crime_incidents WHERE Crime_Type == crime_type GROUP BY Month ;''' %  (strt_year, end_year)
#df = pd.read_sql_query(query, conn)

print(df)

plot = df.plot.bar(x="Month")
plt.plot()
plt.show()
plt.close()

conn.close()
