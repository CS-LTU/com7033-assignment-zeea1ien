import pymongo

# Establish a connection to the MongoDB server
def connect_to_mongodb():
    try:
        mongodb = pymongo.MongoClient("mongodb://localhost:27017")
        print("Connected to MongoDB successfully!")
        return mongodb
    except pymongo.errors.ConnectionError as e:
        print(f"Could not connect to MongoDB: {e}")
        return None

# Function to insert data into MongoDB
def insert_data(data, mongodb):
    try:
        mydatabase = mongodb["StrokeDB"]
        user_collection = mydatabase["PatientCollection"]
        user_collection.insert_one(data)
        print("Data inserted successfully!")
    except pymongo.errors.PyMongoError as e:
        print(f"An error occurred while inserting data: {e}")

