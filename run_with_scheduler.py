import threading
import time
import schedule

from app.main import app  # your FastAPI app
from app.activecampaign import get_all_contacts
from app.activecampaign_sync import sync_contacts_from_activecampaign

def job():
    print("[SYNC] Running scheduled ActiveCampaign sync...")
    try:
        ac_contacts = get_all_contacts(limit=1000)
        sync_contacts_from_activecampaign(ac_contacts)
        print("[SYNC] Sync completed successfully.")
    except Exception as e:
        print(f"[SYNC][ERROR] Sync failed: {e}")

def run_scheduler():
    schedule.every(15).minutes.do(job)
    print("[SCHEDULER] Scheduler started (every 15 minutes).")
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    # Start the scheduler in the background
    t = threading.Thread(target=run_scheduler, daemon=True)
    t.start()

    # Start FastAPI server
    import uvicorn
    print("[API] Starting FastAPI server on http://0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
