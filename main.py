# removed pip install (handled in requirements.txt) mysql-connector-python

!apt-get -y install mysql-server

!service mysql start

!mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH 'mysql_native_password' BY 'root';FLUSH PRIVILEGES;"

import mysql.connector

# Create a connection to the MySQL server
conn = mysql.connector.connect(user='root', password='root', host='localhost')

# Create a cursor to interact with the MySQL server
cursor = conn.cursor()

# Create a new database named 'library'
cursor.execute("CREATE DATABASE IF NOT EXISTS DB_RECEIPE")

# Switch to the 'library' database
cursor.execute("USE DB_RECEIPE")

# Create the 'books' table
cursor.execute('''
CREATE TABLE IndianReceipe(
	ID int NOT NULL,
	RecipeName varchar(500) NULL,
	Ingredients varchar(4000) NULL,
	PrepTimeInMins int NULL,
	CookTimeInMins int NULL,
	TotalTimeInMins int NULL,
	Servings int NULL,
	Cuisine varchar(500) NULL,
	Course varchar(500) NULL,
	Diet varchar(500) NULL,
	Instructions varchar(4000) NULL
)
''')

# Always remember to close the cursor and connection when done
cursor.close()
conn.close()

# removed colab import
uploaded = # removed colab upload (CSV should be in /app/data)
#upload file: 'DataDump.sql' here

!mysql -u root -proot DB_RECEIPE < DataDump.sql

import pandas as pd

# Connect to MySQL
conn = mysql.connector.connect(user='root', password='root', host='localhost', database='DB_RECEIPE')

# Fetch data into a pandas DataFrame
query = "SELECT * FROM IndianReceipe"
df = pd.read_sql(query, conn)

import mysql.connector

# Connect to the MySQL server and the 'library' database
conn = mysql.connector.connect(user='root', password='root', host='localhost', database='DB_RECEIPE')
cursor = conn.cursor()

# Execute the SELECT query
cursor.execute("SELECT * FROM IndianReceipe")

# Fetch all the results
records = cursor.fetchall()

# Print the records
for record in records:
    print(record)

# Close the cursor and connection
cursor.close()
conn.close()

def take_inputs_until_enter():
    inputs = []
    print("Enter Ingridients available: ")
    while True:
        user_input = input()
        if user_input == '':
            break
        inputs.append(user_input)
    return inputs

igds = take_inputs_until_enter()

print("Inputs:", igds)

import pandas as pd
from IPython.display import display
import matplotlib.pyplot as plt

# Connect to the MySQL server and the 'library' database
conn = mysql.connector.connect(user='root', password='root', host='localhost', database='DB_RECEIPE')
cursor = conn.cursor()

conditions = ' AND '.join(f"Ingredients LIKE '%{word}%'" for word in igds)

# Use a SELECT query to retrieve rows that contain any of the specified words
query = f"SELECT * FROM IndianReceipe WHERE {conditions}"

cursor.execute(query)
# Fetch all the rows that match the condition
result = cursor.fetchall()

df = pd.read_sql(query, conn)
#print(df)

pd.set_option('display.max_colwidth', None)

# Define the column name for which you want to increase the width
target_column = 'Instructions'

desired_order = ['RecipeName','Diet','Cuisine','Course','Ingredients','PrepTimeInMins','CookTimeInMins','TotalTimeInMins','Servings','Instructions','ID']

# Reorder the columns in-place
df = df[desired_order]

# Apply some basic styling
styled_df = df.style \
    .set_properties(**{'border': '1px solid black', 'text-align': 'center'}) \
    .set_table_styles([{'selector': 'thead','props': [('max-width', '200px'), ('word-wrap', 'break-word'),('border', '1px solid black')]}])

# Display the styled DataFrame
display(styled_df)

# Plot a graph
plt.figure(figsize=(10, 5))
plt.bar(df['RecipeName'], df['TotalTimeInMins'], color='skyblue')
plt.xticks(rotation=45, ha='right', wrap=True)
plt.xlabel('Recipe Name',wrap=True)
plt.ylabel('Total Time In Mins')
plt.title('Timing')
plt.show()

# Close the cursor and connection
cursor.close()
conn.close()