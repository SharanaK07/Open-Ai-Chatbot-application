import os
from database import init_db

# Delete the old database file if it exists
if os.path.exists("database.db"):
    os.remove("database.db")

# Initialize the database (recreate tables and default admin)
init_db()

print("Database has been reset and initialized successfully.")
