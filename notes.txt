import pandas as pd
from sqlalchemy import create_engine

# Define the path to your SQLite database
database_path = 'sqlite:///Database.db'

# Create a database connection
engine = create_engine(database_path)

# Load the CSV file into a pandas DataFrame
csv_file = 'healthcare-dataset-stroke-data.csv'
df = pd.read_csv(csv_file)

# Display the first few rows of the DataFrame to check the data
print(df.head())

# Write the data to a new table in the SQLite database
table_name = 'stroke_data'  # Name your table here
df.to_sql(table_name, con=engine, if_exists='replace', index=False)

print(f"Data from {csv_file} has been loaded into the {table_name} table in the SQLite database.")

