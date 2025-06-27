from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from ..db import SessionLocal
from .. import crud, schemas, models
from ..activecampaign import get_all_contacts
from ..activecampaign_sync import sync_contacts_from_activecampaign

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/ping")
def ping():
    return {"status": "ok"}

@router.get("/fields")
def get_fields():
    # Update with all required fields for mapping
    return {
        "fields": [
            {"field_id": "first_name_text", "label": "First Name"},
            {"field_id": "last_name_text", "label": "Last Name"},
            {"field_id": "email_text", "label": "Email"},
            {"field_id": "phone_text", "label": "Phone"},
        ]
    }

@router.post("/contact", response_model=schemas.ContactResponse)
def upsert_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    existing = crud.get_contact_by_email(db, contact.email_text)
    if existing:
        updated = crud.update_contact(db, existing, contact.dict(exclude_unset=True))
        return updated
    else:
        new = crud.create_contact(db, contact)
        return new

@router.post("/note")
def add_note(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    return crud.create_note(db, note)

@router.get("/ac-contacts")
def fetch_activecampaign_contacts(limit: int = 100, offset: int = 0):
    """
    Get contacts directly from ActiveCampaign API.
    """
    contacts = get_all_contacts(limit=limit, offset=offset)
    return {"contacts": contacts}

@router.post("/sync-ac-to-mysql")
def sync_ac_to_mysql():
    ac_contacts = get_all_contacts(limit=1000)  # or batch as needed
    sync_contacts_from_activecampaign(ac_contacts)
    return {"status": "sync complete"}
