# ==========================================================
# 📄 IMPORTS
# ==========================================================
from fastapi import FastAPI, HTTPException, Request
from pymongo import MongoClient, errors
from settings import (
    MONGO_URI, MONGO_DB, MONGO_USER_COLLECTION,
    MONGO_CLIENT_COLLECTION, PORT
)
from logger import log  # ✅ Custom logger for all logs

# ==========================================================
# 🗄️ DATABASE CONNECTION SETUP
# ==========================================================
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client[MONGO_DB]
    user_collection = db[MONGO_USER_COLLECTION]
    client_collection = db[MONGO_CLIENT_COLLECTION]
    log.info("✅ MongoDB connected successfully")
except Exception as e:
    log.error(f"❌ MongoDB connection failed: {str(e)}")
    raise

# ==========================================================
# 🚀 FASTAPI APPLICATION INITIALIZATION
# ==========================================================
app = FastAPI(
    title="🎥 Screen Recording Report API",
    version="1.1",
    description="API for managing user and client screen recording reports"
)

# ==========================================================
# 🔧 Helper Function for Standardized Responses
# ==========================================================
def create_response(status: int, message: str, data=None):
    """Utility function to standardize API responses."""
    return {"status": status, "message": message, "data": data or []}


# ==========================================================
# 🧾 POST: Add User Report
# ==========================================================
@app.post("/user_report")
async def add_user_report(request: Request):
    """➕ Insert a new user report document into MongoDB."""
    try:
        data = await request.json()
        if not data:
            raise HTTPException(status_code=400, detail="Request body cannot be empty")

        result = user_collection.insert_one(data)
        log.info(f"🧍‍♂️ User report inserted: {result.inserted_id}")

        return create_response(200, "User report inserted successfully", {"inserted_id": str(result.inserted_id)})

    except errors.PyMongoError as e:
        log.error(f"MongoDB Error in add_user_report: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        log.error(f"Unexpected Error in add_user_report: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inserting user report: {str(e)}")


# ==========================================================
# 🧾 POST: Add Client Report
# ==========================================================
@app.post("/client_report")
async def add_client_report(request: Request):
    """➕ Insert a new client report document into MongoDB."""
    try:
        data = await request.json()
        if not data:
            raise HTTPException(status_code=400, detail="Request body cannot be empty")

        result = client_collection.insert_one(data)
        log.info(f"🏢 Client report inserted: {result.inserted_id}")

        return create_response(200, "Client report inserted successfully", {"inserted_id": str(result.inserted_id)})

    except errors.PyMongoError as e:
        log.error(f"MongoDB Error in add_client_report: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        log.error(f"Unexpected Error in add_client_report: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inserting client report: {str(e)}")


# ==========================================================
# 📋 GET: Fetch All User Reports
# ==========================================================
@app.get("/user_report")
async def get_user_report():
    """📤 Retrieve all user reports."""
    try:
        reports = list(user_collection.find({}, {"_id": 0}))
        log.info(f"Fetched {len(reports)} user reports")
        message = f"Found {len(reports)} user reports" if reports else "No user reports found"
        return create_response(200, message, reports)
    except errors.PyMongoError as e:
        log.error(f"MongoDB Error in get_user_report: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        log.error(f"Unexpected Error in get_user_report: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching user reports: {str(e)}")


# ==========================================================
# 📋 GET: Fetch All Client Reports
# ==========================================================
@app.get("/client_report")
async def get_client_report():
    """📤 Retrieve all client reports."""
    try:
        reports = list(client_collection.find({}, {"_id": 0}))
        log.info(f"Fetched {len(reports)} client reports")
        message = f"Found {len(reports)} client reports" if reports else "No client reports found"
        return create_response(200, message, reports)
    except errors.PyMongoError as e:
        log.error(f"MongoDB Error in get_client_report: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        log.error(f"Unexpected Error in get_client_report: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching client reports: {str(e)}")


# ==========================================================
# 🔍 GET: Check if Report Exists
# ==========================================================
@app.get("/check_report_exists")
async def check_report_exists(clientId: int, macAddress: str):
    """
    ✅ Check if a record exists for a given clientId and macAddress
    in either 'user_report' or 'client_report' collection.
    """
    try:
        # Check in user collection
        user_doc = user_collection.find_one({"clientId": clientId, "macAddress": macAddress})
        if user_doc:
            log.info(f"Record found in user_collection for clientId={clientId}")
            return create_response(200, "Record found in user collection", {
                "exists": True,
                "collection": "user_collection",
                "isValid": user_doc.get("isValid", False)
            })

        # Check in client collection
        client_doc = client_collection.find_one({"clientId": clientId, "macAddress": macAddress})
        if client_doc:
            log.info(f"Record found in client_collection for clientId={clientId}")
            return create_response(200, "Record found in client collection", {
                "exists": True,
                "collection": "client_collection",
                "isValid": client_doc.get("isValid", False)
            })

        log.info(f"No record found for clientId={clientId}, macAddress={macAddress}")
        return create_response(200, "No matching record found", {"exists": False})

    except errors.PyMongoError as e:
        log.error(f"MongoDB Error in check_report_exists: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        log.error(f"Unexpected Error in check_report_exists: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error checking record: {str(e)}")


# ==========================================================
# ✏️ PUT: Update 'isValid' Field in Client Report
# ==========================================================
@app.put("/client_report/update_validity")
async def update_client_report_is_valid(request: Request):
    """🔄 Update the 'isValid' field in a client report."""
    try:
        data = await request.json()
        client_id = data.get("clientId")
        mac = data.get("macAddress")
        is_valid = data.get("isValid")

        # Validate required fields
        if not all([client_id, mac, isinstance(is_valid, bool)]):
            raise HTTPException(status_code=400, detail="clientId, macAddress, and boolean isValid are required")

        result = client_collection.update_one(
            {"clientId": client_id, "macAddress": mac},
            {"$set": {"isValid": is_valid}}
        )

        if result.matched_count == 0:
            log.warning(f"No client report found for clientId={client_id}, mac={mac}")
            return create_response(404, "No matching client report found to update")

        log.info(f"Client report updated for clientId={client_id}, mac={mac}")
        return create_response(200, "Client report updated successfully", {"updated_count": result.modified_count})

    except errors.PyMongoError as e:
        log.error(f"MongoDB Error in update_client_report_is_valid: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        log.error(f"Unexpected Error in update_client_report_is_valid: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating client report: {str(e)}")


# ==========================================================
# ❌ DELETE: Remove a Client Report
# ==========================================================
@app.delete("/client_report/delete")
async def delete_client_report(clientId: int, macAddress: str):
    """
    ❌ Delete a client report from MongoDB based on clientId and macAddress.
    """
    try:
        # Attempt to delete the document
        result = client_collection.delete_one({"clientId": clientId, "macAddress": macAddress})

        if result.deleted_count == 0:
            log.warning(f"No client report found to delete for clientId={clientId}, macAddress={macAddress}")
            return create_response(404, "No matching client report found to delete")

        log.info(f"Client report deleted for clientId={clientId}, macAddress={macAddress}")
        return create_response(200, "Client report deleted successfully", {"deleted_count": result.deleted_count})

    except errors.PyMongoError as e:
        log.error(f"MongoDB Error in delete_client_report: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        log.error(f"Unexpected Error in delete_client_report: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error deleting client report: {str(e)}")


# ==========================================================
# ▶️ RUN THE APPLICATION
# # ==========================================================
# if __name__ == "__main__":
#     import uvicorn
#     log.info(f"🚀 Starting Screen Recording Report API on port {PORT}")
#     uvicorn.run(app, host="0.0.0.0", port=PORT)
