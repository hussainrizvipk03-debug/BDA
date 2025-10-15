# BDA (Big Data Analytics) Course Assignments

This repository contains Big Data Analytics course assignments and projects.

## 📁 Project Structure

```
BDA/
├── BDA course assigment 1/     # Assignment 1
└── BDA LAB 3/                 # Lab 3 - Adobe SDFS Implementation
    ├── main.py                # Adobe SDFS CRUD Application
    ├── docker-compose.yml     # Docker Configuration
    ├── requirements.txt       # Python Dependencies
    ├── .env                   # Environment Variables
    └── sdfs_config/           # Adobe SDFS Configuration
        └── sdfs.conf
```

## 🚀 Adobe SDFS (Simple Distributed File System) - Lab 3

### Overview
Implementation of Adobe's Simple Distributed File System (SDFS) using MongoDB as the backend storage system. This project demonstrates CRUD operations on a distributed file system similar to Adobe's internal file storage system.

### Features
- ✅ **Adobe SDFS Implementation** - Simulates Adobe's distributed file system
- ✅ **Docker Integration** - Containerized application with MongoDB
- ✅ **CRUD Operations** - Complete Create, Read, Update, Delete functionality
- ✅ **Distributed Storage** - Document sharding across multiple shards
- ✅ **Adobe Metadata** - Cloud regions, replication factors, file types

### Technologies Used
- **Python 3.9+**
- **MongoDB** (configured as Adobe SDFS)
- **Docker & Docker Compose**
- **PyMongo** - MongoDB Python driver
- **python-dotenv** - Environment variable management

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd BDA/BDA LAB 3
   ```

2. **Start Adobe SDFS Container**
   ```bash
   docker-compose up -d
   ```

3. **Run the Application**
   ```bash
   python main.py
   ```

### Docker Commands

```bash
# Start Adobe SDFS
docker-compose up -d

# Stop Adobe SDFS
docker-compose down

# View logs
docker-compose logs

# Check container status
docker ps
```

### Adobe SDFS Features

- **Distributed File Paths**: Each document gets a unique SDFS path
- **Sharding**: Documents distributed across shards (shard_a1, shard_b2, etc.)
- **Adobe Metadata**: Cloud regions, replication factors, file types
- **CRUD Operations**: Complete document management system

### Example SDFS Path
```
/adobe/sdfs/shard_a1/documents/abc123def456.json
```

### Container Information
- **Container Name**: ADOBE
- **Port**: 27018:27017
- **Database**: adobe_sdfs
- **Collection**: distributed_documents

## 📚 Course Information
- **Course**: Big Data Analytics (BDA)
- **University**: [Your University Name]
- **Student**: [Your Name]
- **Academic Year**: 2024-2025

## 🔧 Requirements
- Python 3.9+
- Docker & Docker Compose
- MongoDB (via Docker)

## 📝 License
This project is for educational purposes only.
