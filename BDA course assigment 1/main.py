import os
import hashlib
import json
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime

# ------------------ LOAD ENVIRONMENT VARIABLES ------------------
load_dotenv()

# ------------------ ADOBE HDFS CONFIGURATION ------------------
class AdobeHDFS:
    """Adobe Hadoop-like Distributed File System - Simulating Adobe's internal distributed file system"""
    
    def __init__(self):
        self.hdfs_user = "adobe_admin"
        self.hdfs_pass = "adobe_sdfs_pass"
        self.hdfs_db = "adobe_hdfs"
        self.hdfs_port = "27018"
        self.hdfs_host = "localhost"
        self.client = None
        self.db = None
        self.collection = None
        self.connect()
    
    def connect(self):
        """Connect to Adobe HDFS (MongoDB configured as distributed file system)"""
        try:
            hdfs_uri = f"mongodb://{self.hdfs_user}:{self.hdfs_pass}@{self.hdfs_host}:{self.hdfs_port}/"
            self.client = MongoClient(hdfs_uri)
            self.db = self.client[self.hdfs_db]
            self.collection = self.db["distributed_documents"]
            print("[SUCCESS] Connected to Adobe HDFS successfully!")
        except Exception as e:
            print(f"[ERROR] Adobe HDFS connection failed: {e}")
            exit()
    
    def generate_hdfs_path(self, document_id):
        """Generate Adobe HDFS distributed file path"""
        # Simulate Adobe's distributed file system path structure
        hash_value = hashlib.md5(document_id.encode()).hexdigest()
        shard = hash_value[:2]  # First 2 chars for sharding
        return f"/adobe/hdfs/shard_{shard}/documents/{document_id}.json"
    
    def create_document(self, data):
        """Create document in Adobe HDFS with distributed path"""
        document_id = str(hashlib.md5(f"{data['name']}{data['email']}{datetime.now()}".encode()).hexdigest())
        hdfs_path = self.generate_hdfs_path(document_id)
        
        document = {
            "_id": document_id,
            "hdfs_path": hdfs_path,
            "data": data,
            "created_at": datetime.now().isoformat(),
            "adobe_metadata": {
                "shard": hdfs_path.split('/')[3],
                "file_type": "user_document",
                "adobe_cloud_region": "us-west-2",
                "replication_factor": 3
            }
        }
        
        result = self.collection.insert_one(document)
        return result.inserted_id, hdfs_path
    
    def read_documents(self):
        """Read all documents from Adobe HDFS"""
        documents = self.collection.find()
        return list(documents)
    
    def find_document_by_name(self, name):
        """Find document by name in Adobe HDFS"""
        return self.collection.find_one({"data.name": name})
    
    def update_document(self, name, new_email):
        """Update document in Adobe HDFS"""
        result = self.collection.update_one(
            {"data.name": name}, 
            {"$set": {"data.email": new_email, "updated_at": datetime.now().isoformat()}}
        )
        return result.modified_count
    
    def delete_document(self, name):
        """Delete document from Adobe HDFS"""
        result = self.collection.delete_one({"data.name": name})
        return result.deleted_count
    
    def get_hdfs_stats(self):
        """Get Adobe HDFS statistics"""
        total_docs = self.collection.count_documents({})
        
        # Simulate distributed file system stats
        shards = {}
        for doc in self.collection.find({}, {"adobe_metadata.shard": 1}):
            shard = doc.get("adobe_metadata", {}).get("shard", "unknown")
            shards[shard] = shards.get(shard, 0) + 1
        
        return {
            "total_documents": total_docs,
            "shards": shards,
            "hdfs_status": "distributed_active"
        }

# ------------------ INITIALIZE ADOBE HDFS ------------------
try:
    hdfs = AdobeHDFS()
    print("[INFO] Adobe HDFS initialized - Distributed file system ready")
except Exception as e:
    print(f"[ERROR] Adobe HDFS initialization failed: {e}")
    exit()

# ------------------ CRUD OPERATIONS ------------------
def create_user(name, email):
    """Insert a new user document into Adobe HDFS."""
    user_data = {"name": name, "email": email}
    doc_id, hdfs_path = hdfs.create_document(user_data)
    print(f"[SUCCESS] User created in Adobe HDFS!")
    print(f"   Document ID: {doc_id}")
    print(f"   HDFS Path: {hdfs_path}")

def read_users():
    """Fetch and display all users from Adobe HDFS."""
    documents = hdfs.read_documents()
    print("\n[INFO] All Users from Adobe HDFS:")
    for doc in documents:
        print(f"   HDFS Path: {doc['hdfs_path']}")
        print(f"   Name: {doc['data']['name']}")
        print(f"   Email: {doc['data']['email']}")
        print(f"   Shard: {doc['adobe_metadata']['shard']}")
        print(f"   Created: {doc['created_at']}")
        print("-" * 50)

def update_user(name, new_email):
    """Update the email of an existing user in Adobe HDFS."""
    modified_count = hdfs.update_document(name, new_email)
    if modified_count:
        print(f"[SUCCESS] Updated user '{name}' in Adobe HDFS")
    else:
        print("[WARNING] No user found with that name in Adobe HDFS.")

def delete_user(name):
    """Delete a user by name from Adobe HDFS."""
    deleted_count = hdfs.delete_document(name)
    if deleted_count:
        print(f"[SUCCESS] Deleted user '{name}' from Adobe HDFS")
    else:
        print("[WARNING] No user found to delete in Adobe HDFS.")

# ------------------ INTERACTIVE MENU SYSTEM ------------------
def display_menu():
    """Display the main menu options."""
    print("\n" + "="*50)
    print("ADOBE HDFS CRUD OPERATIONS MENU")
    print("="*50)
    print("1. CREATE User")
    print("2. READ All Users")
    print("3. FIND User by Name")
    print("4. UPDATE User Email")
    print("5. DELETE User")
    print("6. SHOW Adobe HDFS Stats")
    print("7. EXIT")
    print("="*50)

def find_user_by_name(name):
    """Find a specific user by name in Adobe HDFS."""
    doc = hdfs.find_document_by_name(name)
    if doc:
        print(f"\n[INFO] User Found in Adobe HDFS:")
        print(f"   Document ID: {doc['_id']}")
        print(f"   HDFS Path: {doc['hdfs_path']}")
        print(f"   Name: {doc['data']['name']}")
        print(f"   Email: {doc['data']['email']}")
        print(f"   Shard: {doc['adobe_metadata']['shard']}")
        print(f"   Created: {doc['created_at']}")
    else:
        print(f"[WARNING] No user found with name '{name}' in Adobe HDFS")

def show_database_stats():
    """Show Adobe HDFS statistics."""
    stats = hdfs.get_hdfs_stats()
    print(f"\n[INFO] Adobe HDFS Statistics:")
    print(f"   Total Documents: {stats['total_documents']}")
    print(f"   HDFS Status: {stats['hdfs_status']}")
    print(f"   Shard Distribution:")
    for shard, count in stats['shards'].items():
        print(f"     {shard}: {count} documents")
    print(f"   Adobe Cloud Region: us-west-2")
    print(f"   Replication Factor: 3")

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
    print("\n[STARTING] Adobe HDFS CRUD Operations Starting...")
    print("[CONNECTING] Connecting to Adobe Hadoop-like Distributed File System...")
    
    # Test connection
    try:
        # Test the Adobe HDFS connection
        hdfs.client.admin.command('ping')
        print("[SUCCESS] Successfully connected to Adobe HDFS!")
        print("[INFO] Distributed file system is ready for document operations")
        
        # Start interactive menu
        interactive_crud()
        
    except Exception as e:
        print(f"[ERROR] Failed to connect to Adobe HDFS: {e}")
        print("\n[TIP] Make sure Docker is running and Adobe HDFS container is started!")
        print("   Run: docker-compose up -d")
