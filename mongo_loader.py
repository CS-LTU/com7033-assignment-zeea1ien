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
        mydatabase = mongodb["User DB"]
        user_collection = mydatabase["User Collection"]
        user_collection.insert_one(data)
        print("Data inserted successfully!")
    except pymongo.errors.PyMongoError as e:
        print(f"An error occurred while inserting data: {e}")

# Function to collect user input
def collect_user_input():
    print("Enter user details:")
    
    name = input("Name: ")
    
    while True:
        age = input("Age: ")
        if age.isdigit():  # Check if age is a valid number
            age = int(age)
            break
        else:
            print("Please enter a valid age (numeric value).")
    
    location = input("Location: ")
    
    # Create a dictionary to hold the user data
    user_data = {
        "name": name,
        "age": age,  # Age is already an integer
        "location": location
    }
    
    return user_data

# Main function to run the program
def main():
    mongodb = connect_to_mongodb()
    if mongodb is None:
        return  # Exit if the connection to MongoDB failed

    # Collect user input
    user_data = collect_user_input()
    
    # Insert the collected data into MongoDB
    insert_data(user_data, mongodb)

    # Optional: Display all documents in the collection
    print("\nAll users in the collection:")
    try:
        mydatabase = mongodb["User DB"]
        user_collection = mydatabase["User Collection"]
        
        for user in user_collection.find({}, {"_id": 0}):  # Exclude the _id field from the output
            print(user)
    except pymongo.errors.PyMongoError as e:
        print(f"An error occurred while retrieving data: {e}")

# Run the main function
if __name__ == "__main__":
    main()

# Close the MongoDB connection when done
if mongodb:
    mongodb.close()