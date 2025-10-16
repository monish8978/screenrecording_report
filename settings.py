# ===============================================
# 📘 SETTINGS CONFIGURATION FILE
# ===============================================
# This file contains all environment-level configurations
# used by the FastAPI "Screen Recording Report API".
# It includes database connection details, logging setup,
# and API server configuration parameters.
# ===============================================


# ==========================
# 🗄️ MongoDB Configuration
# ==========================

# MongoDB connection URI:
# - Uses MongoDB Atlas (cloud-hosted MongoDB service)
# - The format follows:
#   mongodb+srv://<username>:<password>@<cluster-address>/?options
# - Parameters:
#   → retryWrites=true : Enables automatic retry for failed write operations
#   → w=majority       : Ensures writes are acknowledged by a majority of nodes
#   → appName=Cluster0 : Identifies the MongoDB app for diagnostics
MONGO_URI = "mongodb+srv://mongodb:mongodb@cluster0.1nfoz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"


# MongoDB database name:
# - This is the main database used to store
#   both user and client screen recording reports.
MONGO_DB = "screenrecording"


# MongoDB collection for storing user reports
# Each document here represents a single user's
# screen recording metadata or activity.
MONGO_USER_COLLECTION = "user_report"


# MongoDB collection for storing client reports
# Each document here corresponds to a client-side
# recording report or validation record.
MONGO_CLIENT_COLLECTION = "client_report"


# ==========================
# 🌐 FastAPI Server Settings
# ==========================

# Port on which the FastAPI application will run.
# The app will be accessible via:
#   http://<server-ip>:9006/
PORT = 9006


# ==========================
# 🧾 Logging Configuration
# ==========================

# Directory path where all API logs will be stored.
# Ensure this directory exists and the app has write permissions.
LOG_DIR = "/var/log/czentrix/"


# Log file name for storing the screen recording API logs.
# Full log file path will be:
#   /var/log/czentrix/screenrecoding_report.log
# Example logs include:
#   - API request and response metadata
#   - Database connection status
#   - Error traces for debugging
LOG_FILENAME = "screenrecording_report.log"


# ===============================================
# ✅ Summary:
#   - MongoDB Atlas used as primary data store
#   - Separate collections for user and client data
#   - FastAPI runs on port 9006
#   - Logs stored under /var/log/czentrix/
# ===============================================


# --------------------------
# Systemd Service Name
# --------------------------

# ✅ SERVICE_FILE:
# This is the name of the systemd service file, used when managing the app with:
#   - `systemctl status screenrecoding-report`
#   - `systemctl start screenrecoding-report`
SERVICE_FILE = "screenrecording-report"
