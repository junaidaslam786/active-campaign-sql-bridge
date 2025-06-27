from sqlalchemy.orm import Session
from datetime import date
from .models import MainInfoTable, ContactInfoTable
from .schemas import ContactCreate, ContactUpdate, NoteCreate

def get_contact_by_email(db: Session, email: str):
    return db.query(MainInfoTable).filter(MainInfoTable.email_text == email).first()

def create_contact(db: Session, contact: ContactCreate):
    db_contact = MainInfoTable(**contact.dict(exclude_unset=True))
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def update_contact(db: Session, db_contact: MainInfoTable, updates: dict):
    for key, value in updates.items():
        if value is not None and value != "":
            old_value = getattr(db_contact, key)
            if value != old_value:
                # Optionally, log old value in ContactInfoTable
                pass
            setattr(db_contact, key, value)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def create_note(db: Session, note: NoteCreate):
    db_note = ContactInfoTable(
        contact_date=date.today(), 
        **note.dict(exclude_unset=True)
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note
