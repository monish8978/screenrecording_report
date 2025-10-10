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
- **Service Management:** systemd service (`screenrecording-report`)  

---

## ⚙️ Installation & Setup

Run the installation script to set up the environment, install dependencies, and configure the service:

```bash
git clone https://github.com/monish8978/screenrecording_report.git
cd screenrecording_report
chmod +x create_env.sh
./create_env.sh

This script will:

🔧 Create a Python virtual environment

📦 Install all dependencies from requirements.txt

⚙️ Set up a systemd service at /etc/systemd/system/screenrecording-report.service

🔁 Enable and start the screenrecording-report service

✅ Verify that the service is active


▶️ Usage

Once setup is complete, the API will automatically start running as a service.

You can verify this by checking the status:

sudo systemctl status screenrecording-report

It should show something like:

● auto-create-ticket.service - Screen Recording Report FastAPI Service
   Active: active (running)


You can also manually start or stop the service anytime:

sudo systemctl restart screenrecording-report
sudo systemctl stop screenrecording-report


🌐 Accessing the API

Once the service is running, the FastAPI application will be accessible at:

http://<server-ip>:9006


If running locally:

http://0.0.0.0:9006


🗓️ Crontab

The setup also ensures a cron job is added:

*/2 * * * * /Czentrix/apps/screenrecording_report/venv/bin/python /Czentrix/apps/screenrecording_report/service_check.py

This job runs every 2 minutes to check and manage services.

📁 Logs

Logs are stored at:

/var/log/czentrix/screenrecording_report.log


You can monitor logs using:

tail -f /var/log/czentrix/screenrecording_report.log
