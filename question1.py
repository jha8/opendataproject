import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# ================================================================================
# // Q1 
#       Prompt user for range of years and crime type.
#   The month wise total count of the number of the crime incidents occured in the
#   given range is displayed on a bar plot.
# ================================================================================

conn = sqlite3.connect("./a4-sampled.db")
c = conn.cursor()
strt_year = int(input("Enter start year (YYYY):"))
end_year = int(input("Enter end_year (YYYY):"))
crime_type = input("Enter a crime type:")

q1 = '''
    SELECT Month, Crime_Type, COUNT(Incidents_Count)
    From crime_incidents 
    WHERE Crime_Type = '{}' and Year >= {} and Year <= {} 
    GROUP BY Month
'''.format(crime_type,strt_year,end_year)
df = pd.read_sql_query(q1, conn)

print(df)

plot = df.plot.bar(x="Month")
plt.plot()
plt.show()
plt.close()

conn.close()
