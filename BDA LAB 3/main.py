import os
from pymongo import MongoClient
from dotenv import load_dotenv

# ------------------ LOAD ENVIRONMENT VARIABLES ------------------
# Ensure .env file is in the same directory as this script
load_dotenv()

# ------------------ READ VARIABLES ------------------
MONGO_USER = "testuser"
MONGO_PASS = "testpass"
MONGO_DB = "testdb"
MONGO_PORT = "27018"
MONGO_HOST = "localhost"

# ------------------ CONNECT TO MONGODB ------------------
try:
    mongo_uri = f"mongodb://{MONGO_HOST}:{MONGO_PORT}/"
    client = MongoClient(mongo_uri)
    db = client[MONGO_DB]
    collection = db["users"]
    print("[SUCCESS] Connected to MongoDB successfully!")
except Exception as e:
    print(f"[ERROR] MongoDB connection failed: {e}")
    exit()

# ------------------ CRUD OPERATIONS ------------------
def create_user(name, email):
    """Insert a new user document into the collection."""
    user = {"name": name, "email": email}
    result = collection.insert_one(user)
    print(f"[SUCCESS] User created with ID: {result.inserted_id}")

def read_users():
    """Fetch and display all users."""
    users = collection.find()
    print("\n[INFO] All Users:")
    for user in users:
        print(user)

def update_user(name, new_email):
    """Update the email of an existing user."""
    result = collection.update_one({"name": name}, {"$set": {"email": new_email}})
    if result.matched_count:
        print(f"[SUCCESS] Updated {result.modified_count} user(s)")
    else:
        print("[WARNING] No user found with that name.")

def delete_user(name):
    """Delete a user by name."""
    result = collection.delete_one({"name": name})
    if result.deleted_count:
        print(f"[SUCCESS] Deleted user with name '{name}'")
    else:
        print("[WARNING] No user found to delete.")

# ------------------ INTERACTIVE MENU SYSTEM ------------------
def display_menu():
    """Display the main menu options."""
    print("\n" + "="*50)
    print("MONGODB CRUD OPERATIONS MENU")
    print("="*50)
    print("1. CREATE User")
    print("2. READ All Users")
    print("3. FIND User by Name")
    print("4. UPDATE User Email")
    print("5. DELETE User")
    print("6. SHOW Database Stats")
    print("7. EXIT")
    print("="*50)

def find_user_by_name(name):
    """Find a specific user by name."""
    user = collection.find_one({"name": name})
    if user:
        print(f"\n[INFO] User Found:")
        print(f"   ID: {user['_id']}")
        print(f"   Name: {user['name']}")
        print(f"   Email: {user['email']}")
    else:
        print(f"[WARNING] No user found with name '{name}'")

def show_database_stats():
    """Show database statistics."""
    total_users = collection.count_documents({})
    print(f"\n[INFO] Database Statistics:")
    print(f"   Total Users: {total_users}")
    if total_users > 0:
        print(f"   Collection Name: {collection.name}")
        print(f"   Database Name: {db.name}")

def get_user_input():
    """Get user input for name and email."""
    name = input("Enter user name: ").strip()
    email = input("Enter user email: ").strip()
    return name, email

def interactive_crud():
    """Main interactive CRUD interface."""
    while True:
        display_menu()
        choice = input("\nSelect an option (1-7): ").strip()
        
        if choice == "1":
            print("\n[CREATE] CREATE USER")
            print("-" * 20)
            name, email = get_user_input()
            if name and email:
                create_user(name, email)
            else:
                print("[WARNING] Name and email are required!")
                
        elif choice == "2":
            print("\n[READ] ALL USERS")
            print("-" * 20)
            read_users()
            
        elif choice == "3":
            print("\n[FIND] FIND USER BY NAME")
            print("-" * 20)
            name = input("Enter name to search: ").strip()
            if name:
                find_user_by_name(name)
            else:
                print("[WARNING] Name is required!")
                
        elif choice == "4":
            print("\n[UPDATE] UPDATE USER EMAIL")
            print("-" * 20)
            name = input("Enter user name: ").strip()
            new_email = input("Enter new email: ").strip()
            if name and new_email:
                update_user(name, new_email)
            else:
                print("[WARNING] Name and new email are required!")
                
        elif choice == "5":
            print("\n[DELETE] DELETE USER")
            print("-" * 20)
            name = input("Enter name to delete: ").strip()
            if name:
                confirm = input(f"Are you sure you want to delete '{name}'? (y/N): ").strip().lower()
                if confirm == 'y':
                    delete_user(name)
                else:
                    print("[CANCELLED] Deletion cancelled.")
            else:
                print("[WARNING] Name is required!")
                
        elif choice == "6":
            print("\n[STATS] DATABASE STATISTICS")
            print("-" * 20)
            show_database_stats()
            
        elif choice == "7":
            print("\n[GOODBYE] Thank you for using MongoDB CRUD Operations!")
            print("Goodbye!")
            break
            
        else:
            print("[WARNING] Invalid option! Please select 1-7.")
        
        input("\nPress Enter to continue...")

# ------------------ MAIN EXECUTION ------------------
if __name__ == "__main__":
    print("\n[STARTING] MongoDB CRUD Operations Starting...")
    print("[CONNECTING] Connecting to MongoDB...")
    
    # Test connection
    try:
        # Test the connection
        client.admin.command('ping')
        print("[SUCCESS] Successfully connected to MongoDB!")
        
        # Start interactive menu
        interactive_crud()
        
    except Exception as e:
        print(f"[ERROR] Failed to connect to MongoDB: {e}")
        print("\n[TIP] Make sure Docker is running and MongoDB container is started!")
        print("   Run: docker-compose up -d")
