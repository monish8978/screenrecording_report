# 🎥 Screen Recording Report API

A **FastAPI-based REST API** for managing user and client screen recording reports. This project provides endpoints for inserting, retrieving, and validating screen recording reports with **MongoDB** as the primary datastore. Built with robust logging, error handling, and service management.

---

## 🚀 Features

- ✅ Add and fetch **user reports** and **client reports**  
- ✅ Check if a report exists by `clientId` and `macAddress`  
- ✅ Update the `isValid` status of client reports  
- ✅ Standardized API response format  
- ✅ Detailed logging using **TimedRotatingFileHandler**  
- ✅ Threaded service management for automatic startup and monitoring  
- ✅ MongoDB Atlas connection with separate collections for users and clients

---

## 🏗️ Tech Stack

- **Backend Framework:** FastAPI  
- **Database:** MongoDB Atlas  
- **Python Version:** 3.10+ recommended  
- **Logging:** Python `logging` with daily rotation  
- **Service Management:** systemd service (`screenrecoding-report`)  

---

## ⚙️ Installation & Setup

Run the installation script to set up the environment, install dependencies, and configure the service:

```bash
git clone https://github.com/monish8978/auto_create_ticket.git
cd auto_create_ticket
chmod +x create_env.sh
./create_env.sh
